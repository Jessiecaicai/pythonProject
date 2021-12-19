# -*- coding: utf-8 -*-
# @Author  : Jessie
# @Time    : 2021/12/18 11:13 下午
# @Function:
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def feedforward(self,inputs):
