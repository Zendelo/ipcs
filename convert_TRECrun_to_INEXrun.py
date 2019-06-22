import subprocess as sp
import dataparser as dp
import pandas as pd
import pickle

if __name__ == '__main__':

    queries_df = pd.read_pickle("C:\\Users\\liorl\\OneDrive - Altec Business Computing Ltd\\Lior - Do Not Touch!\\Study\\Technion\\Advanced Topics in IR - Technion - 2019\\FInal Project\\ipcsGit\\ipcs\\pkl_files\\queries_df.pkl")
    print(queries_df.columns)
    # exit()
    queries_df.drop('2010061', inplace=True)
    print(len(queries_df))
    inex_run_lines_list = open("bert_inex_converted.run", "w")

    trec_run = open("output_bert_predictions_test.run", 'r')
    for line in trec_run:
        line_parts = line.split()
        qid = line_parts[0]
        pid = line_parts[2].split("_")
        if queries_df.loc[qid == queries_df["bert_qid"]].index[0] == 2009078:
            inex_run_lines_list.write(
                f'2010061 Q0 {pid[0]} {line_parts[3]} {line_parts[4]} TREC2INEX {pid[1]} {pid[2]}\n')
        inex_run_lines_list.write(
            f'{queries_df.loc[queries_df["bert_qid"]==qid].index[0]} Q0 {pid[0]} {line_parts[3]} {line_parts[4]} TREC2INEX {pid[1]} {pid[2]}\n')

    inex_run_lines_list.close()
