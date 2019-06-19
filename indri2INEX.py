import pandas as pd
import dataparser as dp
import subprocess as sp

df = pd.read_csv(f'pass_bm25_baseline.run', sep='\t', header=None, names=['score', 'docNo', 'start_token', 'end_token'])
queries_dict = dp.QueriesXMLParser(f'INEX_queires.xml').text_queries
qids = pd.Series(list(queries_dict.keys()))

indices = []
for val in qids:
    indices.extend([val] * 1000)
df.insert(0, 'qid', indices)
ranks = list(range(1, 1001)) * 120
df.insert(2, 'rank', ranks)

print(df)


def convert_token2char(docno, token):
    dump_index_path = dp.ensure_file('~/ipcs/indri-5.8-install/bin/dumpindex')
    index_path = dp.ensure_dir('~/ipcs/IndexDocsClean5.8')
    docid = sp.run([dump_index_path, index_path, 'di', 'docno', f'{docno}'],
                   capture_output=True, text=True).stdout  # docid 2619640
    positions = sp.run([dump_index_path, index_path, 'dd', f'{docid}'], capture_output=True, text=True).stdout

    for i, line in enumerate(positions.split('\n')):
        if 'Positions' in line:
            first_line = i + 1
        if 'Tags' in line:
            last_line = i - 1
    positions = positions.split('\n')[first_line:last_line]
    pos_df = pd.DataFrame(positions)
    print(pos_df)

    convert_token2char(52502, 4200)
