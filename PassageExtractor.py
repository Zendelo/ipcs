import json
import re
import subprocess as sp
import dataparser as dp
import pandas as pd

dump_index_path = dp.ensure_file('~/ipcs/indri-5.8-install/bin/dumpindex')
index_path = dp.ensure_dir('~/ipcs/IndexDocsClean5.8')

def docno2docid(docno):
    """Converts docNo to docID"""
    return sp.run([dump_index_path, index_path, 'di', 'docno', f'{docno}'], capture_output=True, text=True).stdout.strip('\n')

def load_init_df(init_df_pkl='pkl_files/init_df.pkl', initial_list='initial_list'):
    try:
        init_file = dp.ensure_file(init_df_pkl)
        init_df = pd.read_pickle(init_file)
    except AssertionError:
        init_df = generate_init_df(initial_list)
    return init_df

def generate_init_df(initial_list_path):
    initial_df = pd.read_csv(initial_list_path, delim_whitespace=True, header=None, names=['qid', 'iteration', 'docNo', 'rank', 'score', 'indri'])
    print(initial_df)
    initial_df['docID'] = initial_df['docNo'].apply(docno2docid)
    initial_df.to_pickle('pkl_files/init_df.pkl')
    return initial_df

def extract_passages(file_path):
    initial_df = load_init_df()
    passage_dict = {}
    dealt_docs = set()

    print(initial_df)
    for index, _df in initial_df.groupby(['qid', 'docID']):
        qid = index[0]
        docid = index[1]
        # print(dump
        doctext = sp.run([dumpindex_path, index_path, 'dt', docid], capture_output=True, text=True).stdout
        print(doctext)
        exit()


    #
    #     if not i % 100:
    #         print(f'Hooray! {i} lines passed')
    #     lineParts = line.split()
    #     docName = lineParts[2].decode("utf-8")
    #     queryID = lineParts[0].decode("utf-8")
    #     if queryID not in passage_dict:
    #         passage_dict[queryID] = {}
    #     if docName not in dealt_docs:
    #         dealt_docs.add(docName)
    #         docIndexID = sp.run([f'{dumpindex_path}', f'{index_path}', 'di', 'docno', f'{docName}'],
    #                             capture_output=True, text=True).stdout
    #         docText = sp.run([dumpindex_path, index_path, 'dt', docIndexID], capture_output=True,
    #                          text=True).stdout
    #
    #         startIdx = 0
    #         passageText = ""
    #
    #         with open("cur_doc.tmp", "w") as f:
    #             f.write(docText)
    #
    #         docText = open("cur_doc.tmp", 'r')
    #
    #         while True:
    #             docLine = re.sub(' +', ' ', docText.readline().strip("\n"))
    #             if docLine == "<TEXT>":
    #                 docLine = re.sub(' +', ' ', docText.readline().strip("\n"))
    #                 while docLine != "</TEXT>":
    #                     docLineParts = docLine.split(" ")
    #                     # if current passage is empty (new document or searching for next passage to annotate)
    #                     if passageText == "":
    #                         # if line smaller than min passage length
    #                         if len(docLineParts) < 300:
    #                             # add the whole line to the passage
    #                             passageText += " ".join(docLineParts)
    #                             # go to next line
    #                             docLine = re.sub(' +', ' ', docText.readline().strip("\n"))
    #                         # if line longer than min passage length
    #                         else:
    #                             # get 300 words
    #                             passageText += " ".join(docLineParts[:300])
    #                             docLine = " ".join(docLineParts[300:])
    #                             passage_dict[queryID][
    #                                 str(docName) + "_" + str(startIdx) + "_" + str(len(passageText))] = passageText
    #                             startIdx += len(passageText)
    #                             passageText = ""
    #                     # part of passage already exists
    #                     else:
    #                         if len(docLineParts) < 300 - len(passageText.split(" ")):
    #                             if lineParts != "":
    #                                 passageText += " ".join(docLineParts)
    #                             docLine = re.sub(' +', ' ', docText.readline().strip("\n"))
    #                         else:
    #                             passageText += " ".join(docLineParts[:300])
    #                             docLine = " ".join(docLineParts[300:])
    #                             passage_dict[queryID][
    #                                 str(docName) + "_" + str(startIdx) + "_" + str(len(passageText))] = passageText
    #                             startIdx += len(passageText)
    #                             passageText = ""
    #                 passage_dict[queryID][
    #                     str(docName) + "_" + str(startIdx) + "_" + str(len(passageText))] = passageText
    #                 startIdx += len(passageText)
    #                 passageText = ""
    #             if not docLine:
    #                 break
    # with open('fullPassagesDict.json', 'w') as json_file:
    #     json.dump(passage_dict, json_file)
    # return passage_dict


def main():
    extract_passages("initial_list")


if __name__ == '__main__':
    main()
