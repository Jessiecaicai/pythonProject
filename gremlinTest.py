import numpy as np
import tensorflow as tf
import matplotlib.pylab as plt
from scipy import stats
from scipy.spatial.distance import pdist,squareform
import pandas as pd

################
# note: if you are modifying the alphabet
# make sure last character is "-" (gap)
################

alphabet = "ARNDCQEGHILKMFPSTWYV-"
states = len(alphabet)
a2n = {}
for a,n in zip(alphabet,range(states)):
  a2n[a] = n
#print(a2n)

'''获取氨基酸对应数字编号 不存在的标记为gap'''
def aa2num(aa):
  '''convert aa into num'''
  if aa in a2n: return a2n[aa]
  else: return a2n['-']

'''将注释和序列都放到np数组中'''
def parse_fasta(filename,limit=-1):
  '''function to parse_fasta'''
  header = []
  sequence = []

  lines = open(filename,"r")

  for line in lines:
    '''将字符串末尾空格去掉'''
    line=line.rstrip()
    #if line[0][0]=='>':
    if line[0] == ">":
      if len(header) == limit:
        break
      header.append(line[1:])
      sequence.append([])
    else:
      sequence[-1].append(line)
  lines.close()
  sequence=[''.join(seq) for seq in sequence]
  # print(np.array(sequence)[0])
  # print(np.array(header)[0])
  return np.array(header),np.array(sequence)

def filt_gaps(msa,gap_cutoff=0.5):
  tmp =(msa == states-1).astype(np.float) #19
  non_gaps = np.where(np.sum(tmp.T,-1).T/msa.shape[0]<gap_cutoff)[0]
  return msa[:,non_gaps],non_gaps

