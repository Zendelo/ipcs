import dataparser as dp
import pandas as pd

queries_file = dp.ensure_file('INEX_queries.xml')
q_obj = dp.QueriesXMLParser(queries_file)
queries_dict = q_obj.text_queries
queries_dict = {k: ' '.join(v) for k, v in queries_dict.items()}
print(queries_dict)

df = pd.DataFrame.from_dict(queries_dict, orient='index')
df.index.name = 'qid'
df = df.rename({0: 'query_txt'}, axis=1)
df['bert_qid'] = df['query_txt'].str.replace(' ', '/')
df.to_pickle('pkl_files/queries_df.pkl')



