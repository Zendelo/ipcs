import json
import re
import subprocess as sp
import dataparser as dp


def extractPassages(filePath):
    dumpindexPath = dp.ensure_file("~/ipcs/indri-5.8-install/bin/dumpindex")
    indexPath = dp.ensure_dir("~/ipcs/IndexDocsClean5.8/")
    file = open(filePath, 'rb')
    passageDict = {}
    dealtDocs = set()
    for i, line in enumerate(file):
        if not i % 100:
            print(f'Hooray! {i} lines passed')
        lineParts = line.split()
        docName = lineParts[2].decode("utf-8")
        queryID = lineParts[0].decode("utf-8")
        if queryID not in passageDict:
            passageDict[queryID] = {}
        if docName not in dealtDocs:
            dealtDocs.add(docName)
            docIndexID = sp.check_output(f'{dumpindexPath} {indexPath} di docno {docName}', capture_output=True,
                                         text=True).stdout
            sp.run(f'{dumpindexPath} {indexPath} dt {docIndexID} > temp.txt', shell=True)

            startIdx = 0
            passageText = ""

            docText = open("temp.txt")

            while True:
                docLine = re.sub(' +', ' ', docText.readline().strip("\n"))
                if docLine == "<TEXT>":
                    docLine = re.sub(' +', ' ', docText.readline().strip("\n"))
                    while docLine != "</TEXT>":
                        docLineParts = docLine.split(" ")
                        # if current passage is empty (new document or searching for next passage to annotate)
                        if passageText == "":
                            # if line smaller than min passage length
                            if len(docLineParts) < 300:
                                # add the whole line to the passage
                                passageText += " ".join(docLineParts)
                                # go to next line
                                docLine = re.sub(' +', ' ', docText.readline().strip("\n"))
                            # if line longer than min passage length
                            else:
                                # get 300 words
                                passageText += " ".join(docLineParts[:300])
                                docLine = " ".join(docLineParts[300:])
                                passageDict[queryID][str(docName) + "_" + str(startIdx) + "_" + str(len(passageText))] = passageText
                                startIdx += len(passageText)
                                passageText = ""
                        # part of passage already exists
                        else:
                            if len(docLineParts) < 300 - len(passageText.split(" ")):
                                if lineParts != "":
                                    passageText += " ".join(docLineParts)
                                docLine = re.sub(' +', ' ', docText.readline().strip("\n"))
                            else:
                                passageText += " ".join(docLineParts[:300])
                                docLine = " ".join(docLineParts[300:])
                                passageDict[queryID][str(docName) + "_" + str(startIdx) + "_" + str(len(passageText))] = passageText
                                startIdx += len(passageText)
                                passageText = ""
                    passageDict[queryID][str(docName) + "_" + str(startIdx) + "_" + str(len(passageText))] = passageText
                    startIdx += len(passageText)
                    passageText = ""
                if not docLine:
                    break
    with open('fullPassagesDict', 'w') as json_file:
        json.dump(passageDict, json_file)
    return passageDict


if __name__ == '__main__':
    extractPassages("initial_list")
