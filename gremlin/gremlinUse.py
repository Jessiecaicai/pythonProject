# -*- coding: utf-8 -*-
# @Author  : Jessie
# @Time    : 2021/11/21 6:50 下午
# @Function:
import pandas as pd

import numpy as np
#
# from gremlin import gremlinTest
# from gremlin import gremlinMRF
# from gremlin.gremlinTest import alphabet
from  gremlin import gremlinTensorflow

# parse fasta

#names,seqs = gremlinTest.parse_fasta("gremlin/4FAZA.fas")
#names,seqs = gremlinTest.parse_fasta("gremlin/query_0_aligned.faa")
names,seqs = gremlinTensorflow.parse_fasta("gremlin/query_0.a3m")

# process input sequences
msa = gremlinTensorflow.mk_msa(seqs)

mrf = gremlinTensorflow.GREMLIN(msa)

mtx = gremlinTensorflow.get_mtx(mrf)
gremlinTensorflow.plot_mtx(mtx)

