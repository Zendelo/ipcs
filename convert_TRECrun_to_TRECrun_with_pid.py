import dataparser as dp
import PassageExtractor
import pandas as pd

if __name__ == '__main__':
    initial_res_file = open(dp.ensure_file('~/ipcs/ipcs/initial_list'))
    BERT_res_file = open("ipcsnew_res_list.txt", 'w')
    # passageDict = {'qid': ["2009001", "2009001", "2009001"],
    #                'docno': ["3260094", "3260094", "32600"],
    #                'docid': ["3260094", "3260094", "32600"],
    #                'rank': [1, 1, 0],
    #                'text': ["VERY", "NICE", "INDEED"],
    #                'start_index': ["0", "301", "0"],
    #                'len': ["300", "300", "300"],
    #                'pid': ["3260094_0_300", "3260094_301_300", "32600_0_300"]}
    df = pd.read_pickle(dp.ensure_file('~/ipcs/ipcs/pkl_files/full_df.pkl'))


    for line in initial_res_file:
        qid, _, docno, rank, score, _ = line.split()
        curr_df = df.loc[(df['qid'] == int(qid)) & (df['docno'] == docno)]

        for i, (_, row) in enumerate(curr_df.iterrows()):
            rank = row['rank']
            BERT_res_file.write(f'{qid} Q0 {row["docno"]}_{row["start_idx"]}_{row["length"]} {rank} {score} convert\n')
