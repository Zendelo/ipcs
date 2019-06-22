import dataparser as dp
import PassageExtractor
import pandas as pd

if __name__ == '__main__':
    initial_res_file = open(dp.ensure_file('~/ipcs/ipcs/initial_list'))
    BERT_res_file = open("ipcsnew_res_list.txt", 'w')
    queries_df = pd.read_pickle('~/ipcs/ipcs/pkl_files/queries_df.pkl')

    df = pd.read_pickle(dp.ensure_file('~/ipcs/ipcs/pkl_files/full_df.pkl'))

    for line in initial_res_file:
        qid, _, docno, rank, score, _ = line.split()
        curr_df = df.loc[(df['qid'] == int(qid)) & (df['docno'] == docno)]

        for i, (_, row) in enumerate(curr_df.iterrows()):
            rank = row['rank']
            BERT_res_file.write(f'{queries_df.loc[qid].bert_qid} Q0 {row["docno"]}_{row["start_idx"]}_{row["length"]} {rank} {score} convert\n')
    BERT_res_file.close()
