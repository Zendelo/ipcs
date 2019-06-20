# import dataparser as dp
# from PassageExtractor import extractPassages
import pandas as pd

if __name__ == '__main__':
    initial_res_file = open("initial_list", 'r')
    BERT_res_file = open("C:\\Users\\liorl\\OneDrive - Altec Business Computing Ltd\\Lior - Do Not Touch!\\Study\\Technion\\Advanced Topics in IR - Technion - 2019\\FInal Project\\ipcsGit\\ipcs\\ipcsnew_res_list.txt", 'w')
    passageDict = {'qid': ["2009001", "2009001", "2009001"],
                   'docno': ["3260094", "3260094", "32600"],
                   'docid': ["3260094", "3260094", "32600"],
                   'rank': [1, 1, 0],
                   'text': ["VERY", "NICE", "INDEED"],
                   'start_index': ["0", "301", "0"],
                   'len': ["300", "300", "300"],
                   'pid': ["3260094_0_300", "3260094_301_300", "32600_0_300"]}
    df = pd.DataFrame(passageDict)

    dealt_docs = set()
    for line in initial_res_file:
        qid, _, docno, rank, score, _ = line.split()
        if docno not in dealt_docs:
            dealt_docs.add(docno)
            curr_df = df.loc[(df['qid'] == qid) & (df['docno'] == docno)]
            print(curr_df)
            for i, (_, row) in enumerate(curr_df.iterrows()):
                pid = row['pid']
                BERT_res_file.write(f'{qid} Q0 {pid} {int(rank)+i} {score} convert\n')
