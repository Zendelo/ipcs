from PassageExtractor import extractPassages
import subprocess as sp
import dataparser as dp
import pickle

if __name__ == '__main__':

    initial_res_file = dp.ensure_file("~/ipcs/initial_list")
    passageDict = extractPassages(initial_res_file)
    inex_qrels = dp.ensure_file("~/ipcs/INEX_Qrels.txt")
    temp_file = dp.ensure_file('~/ipcs/INEX_eval.tmp')
    trec_qrels = open("", 'w+')
    trec_qrels_list = []
    for qid in passageDict:
        for pid in passageDict[qid]:
            name_parts = pid.split("_")
            with open(temp_file, "w") as temp:
                temp_path = dp.ensure_file(temp)
                temp.write(f'{qid} Q0 {name_parts[0]} 1 1 yeet {name_parts[1]} {name_parts[2]}')
                rel_ret_size = sp.run(f'java -jar inex_eval.jar -f -q {inex_qrels} {temp_path} |grep rel_ret_size', capture_output=True, text=True).stdout
                rel_ret_size = rel_ret_size.split()[2]
                if rel_ret_size >= 300:
                    trec_qrels_list.append(f'{qid} 1 {pid} 1')
                else:
                    trec_qrels_list.append(f'{qid} 1 {pid} 0')

    with open('trec_qrels_list.pkl', 'wb') as f:
        pickle.dump(trec_qrels_list, f)


