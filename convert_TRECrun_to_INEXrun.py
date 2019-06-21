from PassageExtractor import extractPassages
import subprocess as sp
import dataparser as dp
import pickle

if __name__ == '__main__':

    inex_run_lines_list=[]

    trec_run = open("", 'r')
    for line in trec_run:
        line_parts = line.split()
        pid = line_parts[2].split("_")
        inex_run_lines_list.append(f'{line_parts[0]} Q0 {pid[0]} {line_parts[3]} {line_parts[4]} TREC2INEX {pid[1]} {pid[2]}')

    with open('trec2inex.pkl', 'wb') as f:
        pickle.dump(inex_run_lines_list, f)


