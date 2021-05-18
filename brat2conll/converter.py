#!/usr/bin/env python
import codecs
import click
import os
import re

OUTPUT_FOLDER = 'output'


class BratToCoNLLConverter:

    def __init__(self, bratInputFile, conllInputFile, verbose):
        self.bratInputFileName = bratInputFile
        self.bratInputFileName_new = bratInputFile + '_new.ann'
        self.conllInputFileName = conllInputFile
        self.outfolder = os.path.join('', OUTPUT_FOLDER)
        self.verbose = verbose
        self.__reset__()

    def __reset__(self):
        self.outputFilename = ''
        self.tokens = []

    def convert(self):
        if self.verbose:
            click.echo('Info: Reading file {0}.'.format(self.bratInputFileName))
        with codecs.open(self.bratInputFileName, 'r', 'utf-8') as openedBratFile:
            # print('New version!!!')
            conllLines = self.getBasicInfo(openedBratFile)
            # print(len(conllLines))
            openedBratFile.seek(0)
            self.convertDuolaANN2StandardANN()

            with codecs.open(self.bratInputFileName_new, 'r', 'utf-8') as openedBratFile_new:
                for (i, line) in enumerate(openedBratFile_new):
                    self.__parse(i, line.strip(), conllLines)
            os.remove(self.bratInputFileName_new)

    def convertDuolaANN2StandardANN(self):
        conllLinesT = list()
        conllLinesR = dict()
        with codecs.open(self.bratInputFileName, 'r', 'utf-8') as openedBratFile, codecs.open(self.bratInputFileName_new, 'w', 'utf-8') as openedBratFile_new:
            for i in openedBratFile:
                if i.startswith('T'):
                    l = i.strip()
                    l = re.split('[\t  ]', l)
                    conllLinesT.append([l[0], l[1], int(l[2]), int(l[3]), l[4], l])
                elif i.startswith('R'):
                    l = i.strip()
                    l = re.split('[\t  ]', l)
                    conllLinesR[l[3].split(':')[1]]=[l[0], l[1], l[2], l[3]]

            conllLinesT = sorted(conllLinesT, key=lambda i: i[2])
            # print(conllLinesR)
            last_end_id = 0
            sentence_id = 0
            for each_line in conllLinesT:
                # print(each_line)
                token_id = each_line[-1][0]
                current_end_id = each_line[2]

                if current_end_id - last_end_id >=2 and last_end_id > 0:
                    openedBratFile_new.write('\n')
                    sentence_id = sentence_id + 1
                openedBratFile_new.write('\t'.join(each_line[-1]) + '\n')

                # 有父结点的结点
                if conllLinesR.get(token_id) is not None:
                    openedBratFile_new.write('\t'.join(conllLinesR.get(token_id)) + '\n')
                # 根结点
                elif each_line[0].startswith('T') and len(each_line) > 2 and each_line[1].startswith('hed'):
                    head = '0'
                    deprel = 'HED'
                    misc = '_'

                    id = 'R0'
                    form = each_line[4]
                    xpostag = each_line[1]
                    if '_' in form:
                        # print(form)
                        xpostag = form.split('_')[1]
                        form = form.split('_')[0]

                    segg= form

                    listOfTokens = [id, deprel, 'Arg1:T0', 'Arg2:'+each_line[0]]
                    openedBratFile_new.write('\t'.join(listOfTokens) + '\n')
                else:
                    print("异常：第"+str(sentence_id+1)+'个句子\t'+'\t'.join([each_line[-2],each_line[0]]))
                    head = '000'
                    deprel = 'HED'
                    misc = '_'

                    id = 'R0'
                    form = each_line[4]
                    xpostag = each_line[1]
                    if '_' in form:
                        # print(form)
                        xpostag = form.split('_')[1]
                        form = form.split('_')[0]

                    segg = form

                    listOfTokens = [id, deprel, 'Arg1:T0', 'Arg2:' + each_line[0]]
                    openedBratFile_new.write('\t'.join(listOfTokens) + '\n')

                last_end_id = each_line[3]

            # print(conllLinesT)

            return conllLinesT, conllLinesR

    def getBasicInfo(self, openedBratFile):
        conllLines = list()
        for i in openedBratFile:
            if i.startswith('T'):
                l = i.strip()
                l = re.split('[\t  ]', l)
                conllLines.append([l[0][1:],l[-1],l[-1],'_',l[1]])
                # print(conllLines[-1])
        return conllLines

    def findID(self, id, conllLines):
        form, lemma, xpostag = '', '', ''
        for i in conllLines:
            if i[0] == id:
                form = i[1]
                lemma = i[2]
                xpostag = i[4]
        return form, lemma, xpostag

    def writeToFile(self):
        outfile_name = self.bratInputFileName + ".conll"
        with codecs.open(outfile_name, 'w+', 'utf-8') as outputFile:
            # outputFile.writelines("#new_text=" + self.outputFilename + "\n")
            outputFile.writelines("# ID\tFORM\tFORM\tFORM\tXPOSTAG\tXPOSTAG\tHEAD\tHEAD\tDEPREL\tDEPREL\tMISC\tMISC\n")
            # print(self.tokens)
            id_dict = {}
            last_word_id = 0
            last_sentence_max_word_id = 0
            for id, tok in enumerate(self.tokens):
                if len(tok)>0:
                    id_dict[tok[0]] = id+1

            for id, tok in enumerate(self.tokens):
                # print(tok)
                pos = ''
                if len(tok) >= 7:
                    # print(tok)
                    if not tok[1].endswith('_') and '_' in tok[1]:
                        # 西北民大第一版brat格式，词和词性混在一起
                        pos = tok[1][tok[1].rfind('_')+1:]
                    else:
                        # 第二版格式，词性单列，在根结点的词性前面加上了"hed"
                        pos = tok[3]
                    # print(pos)
                    if pos == 'hed':
                        pos = tok[1][tok[1].rfind('_')+1:]
                    elif pos.startswith('hed'):
                        # print(pos)
                        pos = pos[len('hed'):]

                if len(tok)>1 and '_' in tok[1]:
                    tok[1] = tok[1][0:tok[1].rfind('_')]
                if len(tok)>1 and '_' in tok[2]:
                    tok[2] = tok[2][0:tok[2].rfind('_')]

                last_word_id = last_word_id + 1
                if len(tok) == 0:
                    outputFile.write('\n')

                    last_sentence_max_word_id = last_word_id
                elif tok[4][1:] == '0':
                    outputFile.writelines(
                        str(id-last_sentence_max_word_id + 1) + '\t' + tok[1] + '\t' + tok[1] + '\t' + tok[2] + '\t' + pos  + '\t' + pos + '\t_\t_\t' + '0' + '\t' + '0' + '\t' + tok[5]  + '\t' + tok[5]+
                        '\t' + tok[6] + '\t' + tok[6] +'\n')
                else:
                    outputFile.writelines(
                        str(id-last_sentence_max_word_id+1) + '\t' + tok[1] + '\t' + tok[1] + '\t' + tok[2] + '\t' + pos  + '\t' + pos + '\t_\t_\t' + str(id_dict[tok[4][1:]]-last_sentence_max_word_id) + '\t'  + str(id_dict[tok[4][1:]]-last_sentence_max_word_id) + '\t' + tok[5] + '\t' + tok[5]+
                        '\t' + tok[6] + '\t' + tok[6] +'\n')

    def __parse(self, linenumber, line, conllLines):
        tokenizedLine = re.split('[\t  ]', line)
        listOfTokens = list()

        filename = re.split('[/ .]', self.bratInputFileName)
        self.outputFilename = filename[-2]

        if len(line) == 0:
            self.tokens.append([])
            pass
        # # hed

        # dep
        elif line[0] == 'R':
            tokenizedId = tokenizedLine[3].split(':')

            id = tokenizedId[1][1:]

            form, segm, xpostag = self.findID(id, conllLines)

            tokenizedArg1 = re.split('[: .]', tokenizedLine[2])

            head = tokenizedArg1[1]
            deprel = tokenizedLine[1]
            misc = '_'

            listOfTokens.append(id)
            listOfTokens.append(form)
            listOfTokens.append(segm)
            listOfTokens.append(xpostag)

            listOfTokens.append(head)
            listOfTokens.append(deprel)
            listOfTokens.append(misc)

            self.tokens.append(listOfTokens)

# def main():
#     converter = BratToCoNLLConverter('data/train-sample.ann', 'data/train-sample.conll', verbose=False)
#     converter.convert()
#     converter.writeToFile()
#
# if __name__ == '__main__':
#     main()
