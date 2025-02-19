import pandas as pd
import dataparser as dp
import subprocess as sp
from time import time


def convert_token2char(docno, start_token, end_token):
    dump_index_path = dp.ensure_file('~/ipcs/indri-5.8-install/bin/dumpindex')
    index_path = dp.ensure_dir('~/ipcs/IndexDocsClean5.8')
    docid = sp.run([dump_index_path, index_path, 'di', 'docno', f'{docno}'],
                   capture_output=True, text=True).stdout  # docid 2619640
    positions = sp.run([dump_index_path, index_path, 'dd', f'{docid}'], capture_output=True, text=True).stdout

    for i, line in enumerate(positions.split('\n')):
        if line.startswith('--- Positions ---'):
            first_line = i + 2
        if line.startswith('--- Tags ---'):
            last_line = i - 1
    positions = positions.split('\n')[first_line:last_line]
    pos_df = pd.DataFrame(positions)[0].str.split(expand=True)
    pos_df = pos_df.rename({0: 'token', 1: 'start_char', 2: 'end_char'}, axis=1).set_index('token')
    start_char, _ = pos_df.loc[start_token]
    try:
        _, end_char = pos_df.loc[end_token]
    except KeyError:
        _, end_char = pos_df.loc[str(int(end_token) - 1)]

    return start_char, str(int(end_char) - int(start_char))


def create_main_df():
    df = pd.read_csv(f'pass_bm25_baseline.run', sep='\t', header=None,
                     names=['score', 'docNo', 'start_token', 'end_token'], dtype=str)
    queries_dict = dp.QueriesXMLParser(f'INEX_queires.xml').text_queries
    qids = pd.Series(list(queries_dict.keys()))

    indices = []
    for val in qids:
        indices.extend([val] * 1000)
    df.insert(0, 'qid', indices)
    ranks = list(range(1, 1001)) * 120
    df.insert(2, 'rank', ranks)
    print(df.loc[56999])
    df[['start_char', 'length']] = df.loc[:, ['docNo', 'start_token', 'end_token']].apply(
        (lambda x: convert_token2char(*x)), axis=1, result_type='expand')
    df = df[['qid', 'docNo', 'rank', 'score', 'start_char', 'length']]
    df.to_pickle('base_df.pkl')
    return df


def main():
    try:
        df_pkl = dp.ensure_file('base_df.pkl')
        df = pd.read_pickle(df_pkl)
    except AssertionError:
        df = create_main_df()

    print(['qid', 'it', 'docNo', 'rank', 'score', 'method', 'start_char', 'length'])
    df.insert(1, 'iteration', 'Q0')
    df.insert(5, 'method', 'bm25')

    print(df)
    df.to_csv('testing.res', sep='\t', index=False, header=False)


if __name__ == '__main__':
    main()
