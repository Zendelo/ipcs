import subprocess
import matplotlib.pyplot as plt
import re


def extractPassages(filePath):
    #dumpindexPath = "indri-5.8-install/bin/dumpindex"
    #indexPath = "/data/AdvancedIR/IndexDocsClean5.8/"
    file = open(filePath, 'rb')
    passageDict = {}
    dealtDocs = set()
    for line in file:
        lineParts = line.split()
        docName = lineParts[2].decode("utf-8")
        if docName not in dealtDocs:
            dealtDocs.add(docName)
            #docIndexID = subprocess.check_output([dumpindexPath, indexPath + " di docno" + docName], shell=True)
            #p = subprocess.Popen([dumpindexPath, indexPath + " dt " + docIndexID + " > temp.txt"], shell=True)
            #p.wait()

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
        else:
            print(passageDict.keys())
            exit(0)


if __name__ == '__main__':
    # X = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5,
    #      0.6, 0.7, 0.8, 0.9, 1.0]
    # y = [18.27, 22.41, 23.80, 25.04, 26.04, 26.57,
    #      26.96, 27.17, 26.95, 26.15, 24.98]
    # plt.plot(X, y, 'k', marker="o", label="ST")
    # plt.ylim(18.0, 30.0)
    # plt.xticks(X)
    # plt.xlabel(r'$\lambda$')
    # plt.ylabel("MAP")
    # plt.title("ROBUST")
    # plt.legend()
    # plt.show()
    print("Hi")

    extractPassages("initial_list")
