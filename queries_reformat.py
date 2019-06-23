import dataparser as dp
import pandas as pd

queries_file = dp.ensure_file('INEX_queries.xml')
q_obj = dp.QueriesXMLParser(queries_file)
queries_dict = q_obj.text_queries
queries_dict = {k: ' '.join(v) for k, v in queries_dict.items()}

df = pd.DataFrame.from_dict(queries_dict, orient='index')
df.index.name = 'qid'
df = df.rename({0: 'query_txt'}, axis=1)
df['bert_qid'] = df['query_txt'].str.replace(' ', '/')
print(df.loc[df.duplicated()])
# df.to_pickle('pkl_files/queries_df.pkl')


def reformat_qrels():
    qrels_file = dp.ensure_file('data/qrels')
    qrels_df = pd.read_csv(qrels_file, delim_whitespace=True, names=['qid', 'iter', 'pid', 'relevance'], header=None)
    qrels_df['qid'] = qrels_df['qid'].apply((lambda x: df.loc[str(x)].bert_qid))
    print(qrels_df)
    qrels_df.to_csv('data/qrels', index=False, header=False, sep=' ')


def reformat_runs():
    runs_file = dp.ensure_file('data/run')
    runs_df = pd.read_csv(runs_file, delim_whitespace=True, names=['qid', 'iter', 'pid', 'rank', 'score', 'method'],
                          header=None)
    runs_df['qid'] = runs_df['qid'].apply((lambda x: df.loc[str(x)].bert_qid))
    print(runs_df)
    runs_df.to_csv('data/run_bert', index=False, header=False, sep=' ')
