# -*- coding: utf-8 -*-
# @Author  : Jessie
# @Time    : 2021/11/17 3:58 下午
# @Function:

def getSequence():
    '''
    随机获得fasta文件中的sequence
    :return:
    '''
    with open('/home/data/datacluster/uniclust30_2018_08_fasta/uniclust30_2018_08_seed.fasta') as txt:
        txtData = txt.readlines()
        # print(txtData)

    resultFile = open('resultFile.fasta', 'w')

    count = 1
    number = 800
    sumLength = 0


    for sequence in txtData:
        if count <= 2 * number:
            count = count + 1
            sumLength = sumLength + len(sequence)
            resultFile.write(sequence)
        else:
            break

    resultFile.close()
    print("sequenceAvaLength = " + str(sumLength/number))

getSequence()


def getSequencefromffdata():
    '''
    获得乱码ffdata里的sequence数据
    :return:
    '''
    #with open('/home/data/datacluster/uniref50/dbsearch500Sequence/msaDB_ca3m.ffdata') as txt:
    with open('/home/data/datacluster/uniclust30_2018_08/uniclust30_2018_08_a3m.ffdata') as txt:
        txtData = txt.readlines()
        print(txtData)

#getSequencefromffdata()




