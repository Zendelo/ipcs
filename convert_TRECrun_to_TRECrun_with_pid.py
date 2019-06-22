import dataparser as dp
import PassageExtractor
import pandas as pd

if __name__ == '__main__':
    initial_res_file = open("initial_list", 'r')
    BERT_res_file = open("C:\\Users\\liorl\\OneDrive - Altec Business Computing Ltd\\Lior - Do Not Touch!\\Study\\Technion\\Advanced Topics in IR - Technion - 2019\\FInal Project\\ipcsGit\\ipcs\\ipcsnew_res_list.txt", 'w')
    # passageDict = {'qid': ["2009001", "2009001", "2009001"],
    #                'docno': ["3260094", "3260094", "32600"],
    #                'docid': ["3260094", "3260094", "32600"],
    #                'rank': [1, 1, 0],
    #                'text': ["VERY", "NICE", "INDEED"],
    #                'start_index': ["0", "301", "0"],
    #                'len': ["300", "300", "300"],
    #                'pid': ["3260094_0_300", "3260094_301_300", "32600_0_300"]}
    df = pd.read_pickle("C:\\Users\\liorl\\OneDrive - Altec Business Computing Ltd\\Lior - Do Not Touch!\\Study\\Technion\\Advanced Topics in IR - Technion - 2019\\FInal Project\\ipcsGit\\ipcs\\pkl_files\\full_df.pkl")


    dealt_docs = set()
    for line in initial_res_file:
        qid, _, docno, rank, score, _ = line.split()
        dealt_docs.add(docno)
        curr_df = df.loc[(df['qid'] == int(qid)) & (df['docno'] == docno)]

        for i, (_, row) in enumerate(curr_df.iterrows()):
            rank = row['rank']
            BERT_res_file.write(f'{qid} Q0 {row["docno"]}_{row["start_idx"]}_{row["length"]} {rank} {score} convert\n')
