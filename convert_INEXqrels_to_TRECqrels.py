import PassageExtractor.extractPassages
import subprocess as sp
import dataparser as dp

if __name__ == '__main__':

    passageDict = extractPassages("")
    inex_qrels = open("", 'r')
    trec_qrels = open("", 'w+')
    trec_qrels_list = []
    for qid in passageDict:
        for pid in passageDict[qid]:
            name_parts = pid.split("_")
            with open("", "w") as temp:
                temp_path = dp.ensure_file(temp)
                temp.write(f'{qid} Q0 {name_parts[0]} 1 1 yeet {name_parts[1]} {name_parts[2]}')
                rel_ret_size = sp.run(f'java -jar inex_eval.jar -f -q INEX_Qrels {temp_path} |grep rel_ret_size', capture_output=True, text=True).stdout
                rel_ret_size = rel_ret_size.split()[2]
                if rel_ret_size >= 300:
                    trec_qrels_list.append(f'{qid} 1 {pid} 1')
                else:
                    trec_qrels_list.append(f'{qid} 1 {pid} 0')

    # for line in inex_qrels.readlines():
    #     lineParts = line.split()
    #     passages = lineParts[6:]
    #     for passage in passages:
    #         # write line in format: qid 0 docid_startidx_lengthOfPassage 1
    #         trec_line = f'{lineParts[0]} 0 {lineParts[2]}_{passage.replace(":","_")} 1'


