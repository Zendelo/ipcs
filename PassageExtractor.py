import json
import subprocess as sp

import pandas as pd

import dataparser as dp


def docno2docid(docno):
    """Converts docNo to docID"""
    return sp.run([dump_index_path, index_path, 'di', 'docno', f'{docno}'], capture_output=True,
                  text=True).stdout.strip('\n')


def load_init_df(init_df_pkl='pkl_files/init_df.pkl', initial_list='initial_list'):
    try:
        init_file = dp.ensure_file(init_df_pkl)
        init_df = pd.read_pickle(init_file)
    except AssertionError:
        init_df = generate_init_df(initial_list)
    return init_df


def generate_init_df(initial_list_path):
    initial_df = pd.read_csv(initial_list_path, delim_whitespace=True, header=None,
                             names=['qid', 'iteration', 'docNo', 'rank', 'score', 'indri'], dtype={'docNo': str})
    initial_df['docID'] = initial_df['docNo'].apply(docno2docid)
    initial_df.to_pickle('pkl_files/init_df.pkl')
    return initial_df


def extract_docs(dict_file_json):
    initial_df = load_init_df()
    docs_dict = {}

    for index, _df in initial_df.groupby(['qid', 'docID']):
        qid = index[0]
        docid = index[1]
        if docid in docs_dict:
            continue
        doctext = sp.run([dump_index_path, index_path, 'dt', docid], capture_output=True, text=True).stdout.split()
        doctxt_st = ' '.join(doctext[3:-2])
        docs_dict[docid] = doctxt_st
    with open(dict_file_json, 'w') as json_file:
        json_file.write(json.dump(docs_dict))
    return docs_dict


def extract_passages(initial_list_path):
    dict_file = f'{pkl_dir}/docs_txt_dict.json'
    n = 300  # passages len in tokens
    try:
        dict_file = dp.ensure_file(dict_file)
        with open(dict_file, 'r') as json_data:
            docs_dict = json.load(json_data)
    except AssertionError:
        print(f'failed to load {dict_file}, will generate a new one and save')
        docs_dict = extract_docs(dict_file)
    passages_dict = {}
    for docid, doctxt in docs_dict.items():
        txt_list = doctxt.split()
        passages_list = [txt_list[i * n:(i + 1) * n] for i in range((len(txt_list) + n - 1) // n)]
        _txt = ' '.join(passages_list[0])
        passages_dict[docid] = {(0, len(_txt)): _txt}
        char_idx = 0
        for i, txt in enumerate(passages_list[1:], 1):
            char_idx += len(' '.join(passages_list[i - 1]))
            txt = ' '.join(txt)
            passages_dict[docid][char_idx, len(txt)] = txt
    return passages_dict


def convert_df(init_df: pd.DataFrame, psg_dict: dict):
    records = []
    init_df = init_df.drop('rank', axis=1)
    for row in init_df.itertuples():
        _, qid, iteration, docno, score, indri, docid = row
        for (start_idx, length), txt in psg_dict[docid].items():
            records.append((qid, iteration, docno, indri, docid, score, start_idx, length, txt))
    df = pd.DataFrame(records,
                      columns=['qid', 'iteration', 'docno', 'indri', 'docid', 'score', 'start_idx', 'length', 'txt'])
    ranks = []
    for qid, _df in df.groupby('qid'):
        ranks.extend(list(range(1, len(_df) + 1)))
    df.insert(5, 'rank', ranks)
    df.insert(7, 'method', 'bm25-indri')
    inex_df = df.loc[:, ['qid', 'iteration', 'docno', 'rank', 'score', 'method', 'start_idx', 'length']]
    inex_df.to_csv('bm25_indri.run', sep=' ', index=False, header=False)
    df.to_pickle(f'{pkl_dir}/full_df.pkl')
    return df


def main():
    initial_df = load_init_df()
    passages_dict = extract_passages("initial_list")
    convert_df(initial_df, passages_dict)


if __name__ == '__main__':
    """Setting the paths in the global namespace"""
    pkl_dir = dp.ensure_dir('~/ipcs/ipcs/pkl_files')
    dump_index_path = dp.ensure_file('~/ipcs/indri-5.8-install/bin/dumpindex')
    index_path = dp.ensure_dir('~/ipcs/IndexDocsClean5.8')
    main()
