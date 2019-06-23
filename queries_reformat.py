import dataparser as dp
import pandas as pd
from glob import glob

queries_file = dp.ensure_file('INEX_queries.xml')
q_obj = dp.QueriesXMLParser(queries_file)
queries_dict = q_obj.text_queries
queries_dict = {k: ' '.join(v) for k, v in queries_dict.items()}

df = pd.DataFrame.from_dict(queries_dict, orient='index')
df.index.name = 'qid'
df = df.rename({0: 'query_txt'}, axis=1)
df['bert_qid'] = df['query_txt'].str.replace(' ', '/')


# print(df.loc[df.duplicated()])


# df.to_pickle('pkl_files/queries_df.pkl')

# def reformat_topics():
#     topic_files = glob('data/*.topics')
#     for fname in topic_files:
#         file_name = fname.split('/')[1]
#         topics_df = pd.read_csv(fname, sep='\t', names=['qid', 'text', 'bert_qid'], header=None)
#         print(topics_df)


def reformat_qrels():
    qrel_files = glob('data/*.qrels')
    for fname in qrel_files:
        file_name = fname.split('/')[1]
        qrels_df = pd.read_csv(fname, delim_whitespace=True, names=['qid', 'iter', 'pid', 'relevance'], header=None)
        qrels_df['qid'] = qrels_df['qid'].apply((lambda x: df.loc[str(x)].bert_qid))
        qrels_df.to_csv(f'treccar_dataset/{file_name}', index=False, header=False, sep=' ')
        print(f'the len of {file_name} is {len(qrels_df)}')


def reformat_runs():
    run_files = glob('data/*.run')
    for fname in run_files:
        file_name = fname.split('/')[1]
        runs_df = pd.read_csv(fname, delim_whitespace=True, names=['qid', 'iter', 'pid', 'rank', 'score', 'method'],
                              header=None)
        runs_df['qid'] = runs_df['qid'].apply((lambda x: df.loc[str(x)].bert_qid))
        runs_df.to_csv(f'treccar_dataset/{file_name}', index=False, header=False, sep=' ')
        print(f'the len of {file_name} is {len(runs_df)}')


if __name__ == '__main__':
    # reformat_topics()
    reformat_runs()
    reformat_qrels()
