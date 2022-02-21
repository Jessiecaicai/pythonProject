import esm
import torch.nn as nn
import torch

model, alphabet = esm.pretrained.esm1b_t33_650M_UR50S()
state_dict = model
