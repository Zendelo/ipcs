import subprocess
from subprocess import run
import matplotlib.pyplot as plt
import re


def extractPassages(filePath):
    dumpindexPath = "../indri-5.8-install/bin/dumpindex"
    indexPath = "../IndexDocsClean5.8/"
    file = open(filePath, 'rb')
    passageDict = {}
    dealtDocs = set()
    for line in file:
        lineParts = line.split()
        docName = lineParts[2].decode("utf-8")
        if docName not in dealtDocs:
            dealtDocs.add(docName)
            docIndexID = subprocess.check_output(f'{dumpindexPath} {indexPath} di docno {docName}', shell=True, text=True).strip()
            run('ls -la > temp' , shell=True)
            run(f'{dumpindexPath} {indexPath} dt {docIndexID} > temp.txt', shell=True)

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
                                passageDict[str(docName) + "_" + str(startIdx) + "_" + str(len(passageText))] = passageText
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
                                passageDict[str(docName) + "_" + str(startIdx) + "_" + str(len(passageText))] = passageText
                                startIdx += len(passageText)
                                passageText = ""
                    passageDict[str(docName) + "_" + str(startIdx) + "_" + str(len(passageText))] = passageText
                    startIdx += len(passageText)
                    passageText = ""
                if not docLine:
                    break


if __name__ == '__main__':
    print("Hi")
    extractPassages("initial_list")
