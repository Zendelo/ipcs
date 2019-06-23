import pandas as pd
import dataparser as dp
import numpy as np
import sklearn

queries_file = dp.ensure_file('~/repos/ipcs/pkl_files/queries_df.pkl')
queries_df = pd.read_pickle(queries_file)
queries_df = sklearn.utils.shuffle(queries_df)
fold_1 = queries_df.iloc[:60]
fold_2 = queries_df.iloc[60:120]
fold_1.to_csv('data/train_set_1.topics', sep='\t', header=False)
fold_2.to_csv('data/test_set_1.topics', sep='\t', header=False)
fold_1.to_csv('data/test_set_2.topics', sep='\t', header=False)
fold_2.to_csv('data/train_set_2.topics', sep='\t', header=False)

runs_df = pd.read_csv('data/run', delim_whitespace=True, header=None,
                      names=['qid', 'iteration', 'pid', 'rank', 'score', 'method'])
runs_df_1 = runs_df.loc[runs_df['qid'].isin(fold_1.index)]
runs_df_2 = runs_df.loc[runs_df['qid'].isin(fold_2.index)]
runs_df_1.to_csv('data/train_set_1.run', sep='\t', header=False)
runs_df_2.to_csv('data/test_set_1.run', sep='\t', header=False)
runs_df_1.to_csv('data/test_set_2.run', sep='\t', header=False)
runs_df_2.to_csv('data/train_set_2.run', sep='\t', header=False)

qrels_df = pd.read_csv('data/qrels', delim_whitespace=True, header=None, names=['qid', 'iteration', 'pid', 'rel'])
qrels_df_1 = qrels_df.loc[qrels_df['qid'].isin(fold_1.index)]
qrels_df_2 = qrels_df.loc[qrels_df['qid'].isin(fold_2.index)]
qrels_df_1.to_csv('data/train_set_1.qrels', sep='\t', header=False)
qrels_df_2.to_csv('data/test_set_1.qrels', sep='\t', header=False)
qrels_df_1.to_csv('data/test_set_2.qrels', sep='\t', header=False)
qrels_df_2.to_csv('data/train_set_2.qrels', sep='\t', header=False)
