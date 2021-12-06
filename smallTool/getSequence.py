# -*- coding: utf-8 -*-
# @Author  : Jessie
# @Time    : 2021/11/17 3:58 下午
# @Function:
import random
from Bio import SeqIO
def getSequenceInturn():
    '''
    顺序获得fasta文件中的sequence
    :return:
    '''
    with open('/home/guo/data/datacluster/uniref50/db/uniref50.fasta') as txt:
        txtData = txt.readlines()
        # print(txtData)

    resultFile = open('resultFile.fasta', 'w')

    count = 1
    number = 50000
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

#getSequenceInturn()

def getSequenceRandom():
    '''
    随机获取特定条数的fasta文件里的sequence(未完成
    :return:
    '''
    with open('/home/guo/data/datacluster/uniref50/db/uniref50.fasta')as txt:
        txtData = txt.readlines()
    #print(txtData)
    resultFile = open('resultSequence.fasta','w')

    count = 1
    number = 5000 # count为所取sequence条数

    while count <= number:
        count = count + 1
        randomNumber = random.randint(1,len(txtData))
        print("len(txtData)为：" + str(len(txtData)))
        resultFile.write(txtData[randomNumber])

    resultFile.close()

#getSequenceRandom()

def getSequenceInturnBio():
    '''
    bio解析+顺序获取特定条数fasta文件里的sequence
    :return:
    '''

    count = 1
    number = 50000
    resultFile = open('resultBioInturnSequence.fasta','w')

    for seq_record in SeqIO.parse('/home/guo/data/datacluster/uniref50/db/uniref50.fasta','fasta'):
        count = count + 1
        if(count < number):
            record = seq_record
            resultFile.write('>' + record.description + '\r\n')
            resultFile.write(str(record.seq) + '\r\n')

    resultFile.close()

getSequenceInturnBio()



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




