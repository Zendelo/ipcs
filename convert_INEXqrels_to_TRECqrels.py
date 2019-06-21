import subprocess as sp
import dataparser as dp
import pandas as pd
import pickle

if __name__ == '__main__':

    # initial_res_file = dp.ensure_file("~/ipcs/initial_list")
    passageDict = pd.read_pickle(
        "C:\\Users\\liorl\\OneDrive - Altec Business Computing Ltd\\Lior - Do Not Touch!\\Study\\Technion\\Advanced Topics in IR - Technion - 2019\\FInal Project\\ipcsGit\\ipcs\\pkl_files\\full_df.pkl")
    inex_qrels = "C:\\Users\\liorl\\OneDrive - Altec Business Computing Ltd\\Lior - Do Not Touch!\\Study\\Technion\\Advanced Topics in IR - Technion - 2019\\FInal Project\\ipcsGit\\ipcs\\INEX_Qrels.txt"
    temp_file = 'C:\\Users\\liorl\\OneDrive - Altec Business Computing Ltd\\Lior - Do Not Touch!\\Study\\Technion\\Advanced Topics in IR - Technion - 2019\\FInal Project\\ipcsGit\\ipcs\\INEX_eval.tmp'
    trec_qrels = open("C:\\Users\\liorl\\OneDrive - Altec Business Computing Ltd\\Lior - Do Not Touch!\\Study\\Technion\\Advanced Topics in IR - Technion - 2019\\FInal Project\\ipcsGit\\ipcs\\trec_bert_qrels.txt", 'w+')
    trec_qrels_list = []
    for row in passageDict.drop(['rank', 'method'], axis=1).itertuples():

        _, qid, iteration, docno, _, _, score, start_idx, length, _ = row
        with open(temp_file, "w") as temp:
            temp_path = temp_file
            temp.write(f'{qid} Q0 {docno} 1 1 yeet {start_idx} {length}')
            rel_ret_size = sp.run(f'java -jar inex_eval.jar -f -q {inex_qrels} {temp_path} |grep rel_ret_size',
                                  capture_output=True, text=True).stdout
            print(rel_ret_size)
            rel_ret_size = rel_ret_size.split()[2]
            exit()
            if int(rel_ret_size) >= 300:
                trec_qrels.write(f'{qid} 1 {docno}_{start_idx}_{length} 1')

            else:
                trec_qrels.write(f'{qid} 1 {docno}_{start_idx}_{length} 0')

    with open('trec_qrels_list.pkl', 'wb') as f:
        pickle.dump(trec_qrels_list, f)
