
## txt2fasta
with open('/home/guo/data/sequenceDesign/twintowersUse12.6_100/12.txt') as txt:
    txtData = txt.readlines()
    #print(txtData)
fastaFile = open('/home/guo/data/sequenceDesign/twintowersUse12.6_100/12.fasta','w')

countInt = 0
for sequence in txtData:
    countInt = countInt+1
    countString = str(countInt)
    fastaFile.write('>'+countString)
    fastaFile.write('\n'+sequence)
    #print(sequence)

fastaFile.close()
