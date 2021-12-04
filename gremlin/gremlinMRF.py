import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_eager_execution()
import matplotlib.pylab as plt
from scipy import stats
from scipy.spatial.distance import pdist,squareform
import pandas as pd
def normalize(x):
    x = stats.boxcox(x - np.amin(x) + 1.0)[0]
    x_mean = np.mean(x)
    x_std = np.std(x)
    return ((x - x_mean) / x_std)


def get_mtx(mrf):
    '''get mtx given mrf'''

    # l2norm of 20x20 matrices (note: we ignore gaps)
    raw = np.sqrt(np.sum(np.square(mrf["w"][:, :-1, :-1]), (1, 2)))
    raw_sq = squareform(raw)

    # apc (average product correction)
    ap_sq = np.sum(raw_sq, 0, keepdims=True) * np.sum(raw_sq, 1, keepdims=True) / np.sum(raw_sq)
    apc = squareform(raw_sq - ap_sq, checks=False)

    mtx = {"i": mrf["w_idx"][:, 0],
           "j": mrf["w_idx"][:, 1],
           "raw": raw,
           "apc": apc,
           "zscore": normalize(apc)}
    return mtx


def plot_mtx(mtx, key="zscore", vmin=1, vmax=3):
    '''plot the mtx'''
    plt.figure(figsize=(5, 5))
    plt.imshow(squareform(mtx[key]), cmap='Blues', interpolation='none', vmin=vmin, vmax=vmax)
    plt.grid(False)
    plt.show()

