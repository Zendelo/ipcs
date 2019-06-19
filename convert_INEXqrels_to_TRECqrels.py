if __name__ == '__main__':

    inex_qrels = open("", 'r')
    trec_qrels = open("", 'w+')
    for line in inex_qrels.readlines():
        lineParts = line.split()
        passages = lineParts[6:]
        for passage in passages:
            # write line in format: qid 0 docid_startidx_lengthOfPassage 1
            trec_line = f'{lineParts[0]} 0 {lineParts[2]}_{passage.replace(":","_")} 1'


