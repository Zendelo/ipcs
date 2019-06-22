import subprocess as sp
import dataparser as dp
import pandas as pd
import pickle

if __name__ == '__main__':

    # initial_res_file = dp.ensure_file("~/ipcs/initial_list")
    queries_df = pd.read_pickle('~/ipcs/ipcs/pkl_files/queries_df.pkl')
    passageDict = dp.ensure_file("~/ipcs/ipcs/pkl_files/full_df.pkl")
    passageDict = pd.read_pickle(passageDict)
    inex_qrels = dp.ensure_file("~/ipcs/INEX_Qrels.txt")
    temp_file = "INEX_eval.tmp"
    trec_qrels = open("trec_bert_qrels.txt", 'w+')
    trec_qrels_list = []
    for row in passageDict.drop(['rank', 'method'], axis=1).itertuples():

        _, qid, iteration, docno, _, _, score, start_idx, length, _ = row
        with open(temp_file, "w") as temp:
            temp_path = temp_file
            temp.write(f'{qid} Q0 {docno} 1 1 yeet {start_idx} {length}')
        inex_eval = dp.ensure_file('~/ipcs/inex_eval.jar')
        rel_ret_size = sp.run(['/usr/bin/java', '-jar', inex_eval, '-f', '-q', inex_qrels, temp_path], capture_output=True).stdout
        rel_ret_size = sp.run(['grep', 'rel_ret_size'], input=rel_ret_size, capture_output=True).stdout
        rel_ret_size = sp.run(['grep', '-v', 'all'], input=rel_ret_size, capture_output=True).stdout
        rel_ret_size = rel_ret_size.split()[2]
        if int(rel_ret_size) >= 300:
            trec_qrels.write(f'{queries_df.loc[qid].bert_qid} 1 {docno}_{start_idx}_{length} 1\n')

        else:
            trec_qrels.write(f'{queries_df.loc[qid].bert_qid} 1 {docno}_{start_idx}_{length} 0\n')

