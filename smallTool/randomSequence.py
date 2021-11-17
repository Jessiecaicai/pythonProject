# -*- coding: utf-8 -*-
# @Author  : Jessie
# @Time    : 2021/11/17 3:58 下午
# @Function:
from smallTool.txtToFasta import txtData
def getSequence():
    with open('/home/data/uniclust30_2018_08_fasta/uniclust30_2018_08_seed.fasta') as txt:
        txtData = txt.readlines()
        # print(txtData)

    resultFile = open('resultFile.fasta', 'w')

    count = 1
    number = 1500
    sumLength = 0

    for sequence in txtData:
        if count <= 2 * number:
            count = count + 1
            resultFile.write(sequence)
        else:
            break

    resultFile.close()



