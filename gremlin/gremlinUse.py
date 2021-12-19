# -*- coding: utf-8 -*-
# @Author  : Jessie
# @Time    : 2021/11/21 6:50 下午
# @Function:
import pandas as pd

import numpy as np

from gremlin import gremlinTest
from gremlin import gremlinMRF
from gremlin.gremlinTest import alphabet

# parse fasta
#names,seqs = gremlinTest.parse_fasta("gremlin/4FAZA.fas")
names,seqs = gremlinTest.parse_fasta("short3AlignedSequence.faa")


# process input sequences
msa = gremlinTest.mk_msa(seqs)

mrf = gremlinTest.GREMLIN(msa)

mtx = gremlinMRF.get_mtx(mrf)
gremlinMRF.plot_mtx(mtx)

