# -*-coding:utf-8-*-
import os
import argparse
import numpy as np
import torch
from scipy.io.arff.tests.test_arffread import data_path
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from apex.parallel import convert_syncbn_model
import param_esm1b
import loadingData
import esm
import torch.nn as nn
import sys
from apex import amp
import glob
from tqdm import tqdm
import torch.nn.functional as F
import time
import math

#os.environ["RANK"] = "0"
os.environ['MASTER_ADDR'] = 'localhost'
os.environ['MASTER_PORT'] = '5678'
#os.environ['WORLD_SIZE'] = '1'
# DDP 多机多卡需要保证初始化的模型相同
def init_seeds(SEED=1):
    torch.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # torch.backends.cudnn.enabled = False # AMP requires torch.backends.cudnn.enabled = True
    # 实验表明不设置这个模型初始化并不会受到影响
    np.random.seed(SEED)
    torch.cuda.manual_seed_all(SEED)

# 对所有的GPU上的loss求平均，打印输出
def reduce_loss(value,average=True):
    world_size = torch.distributed.get_world_size()
    if world_size < 2:  # 单个GPU的情况直接输出
        return value

    with torch.no_grad():
        output_tensors = value.clone()
        torch.distributed.all_reduce(output_tensors) # 所有GPU上的loss求和
        if average:
            output_tensors /= world_size
        return output_tensors

# 1）多机多卡的初始化
# 在调用任何其他方法之前，初始化该distributed包。可组织所有进程加入
# backend 要使用的后端的名称
torch.distributed.init_process_group(backend = 'nccl')

# 2）从外边获得local_rank的参数，多机多卡的torch.distributed.launch会传给这个参数
'''parser = argparse.ArgumentParser()
parser.add_argument('--local_rank', default=-1,type=int, help='node rank for distributed training')
args = parser.parse_args()'''

args = param_esm1b.params_parser()

# 3）设置cuda
# local_rank = torch.distributed.get_rank()
torch.cuda.set_device(args.local_rank)
# device = torch.device("cuda",args.local_rank)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == '__main__':
    # 初始化参数
    epochs = 20000
    batch_size = 24
    learning_rate = 5e-5
    Seed = 2021
    init_seeds(SEED=Seed)
    # 加载训练数据
    # train_dataset = loadingData.AllDataset()
    # train_sample = torch.utils.data.distributed.DistributedSampler(train_dataset)
    # train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=False, drop_last=True,
    #                           collate_fn=train_dataset.collate__fn, sampler=train_sample)
    data_path = '/home/guo/pythonProject/chenlei/protein_representation_learning/data/downstream'
    fluorescence_train_data = loadingData.datasetGetCL.FluorescenceDataset(data_path, 'train')

    # 初始化模型
    # args_model = param_esm1b.params_parser()
    esm1b_alphabet = esm.data.Alphabet.from_architecture(args.arch)
    model = esm.model.ProteinBertModel(args, esm1b_alphabet)
    # Premodel = esm.model.ProteinBertModel(args, esm1b_alphabet)
    # model = esm.model.SmallSampleContainProteinBertModel(Premodel)

    # for name, parameters in model.named_parameters():
    #     print(name, ':', parameters.size())

    model = model.to(device)
    criterion = nn.CrossEntropyLoss(ignore_index=-1)

    model = convert_syncbn_model(model)         # 在使用nn.DistributedDataParallel时，用nn.SyncBatchNorm替换或包装nn.BatchNorm层。
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    model, optimizer = amp.initialize(model, optimizer, opt_level='O2')

    model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.local_rank], output_device=args.local_rank, find_unused_parameters=True)
    model.to(device)

    model.train()
    for epoch_item in range(epochs):
        train_loader.sampler.set_epoch(epoch_item)
        training_loss = 0
        training_step = 0
        training_step_out = 0
        for i, data in enumerate(train_loader):
            tokens, all_label_ids = data
            tokens,all_label_ids = tokens.cuda(),all_label_ids.cuda()

            results = model(tokens, return_contacts=False)
            logits = results["logits"].cuda()

            loss = criterion(logits.contiguous().view(-1, len(esm1b_alphabet.all_toks)),all_label_ids.contiguous().view(-1))
            training_loss += loss
            training_step += 1
            training_step_out += 1

            optimizer.zero_grad()
            with amp.scale_loss(loss,optimizer) as scaled_loss:
                scaled_loss.backward()
            optimizer.step()

            if training_step_out % 1000 == 0:
                training_loss /= training_step_out     # 迭代1000次的平均loss
                reduceLOSS = reduce_loss(training_loss)
                if args.local_rank == 0:               # 在每台机器上都输出loss
                    print("Epoch: {}. \t Step: {} / {} finish. \t Training Loss: {:.5f}.".format(epoch_item, training_step, len(train_loader), reduceLOSS.item()))
                if torch.distributed.get_rank() == 0:  # 在第一台机器的第一张卡上保存loss
                    with open("../log/loss.txt","a+") as out_loss:
                        out_loss.write("Epoch: {} \t Step: {} / {} finish. \t Average Loss (1000iter): {:.5f}.\n".format(epoch_item, training_step,len(train_loader),reduceLOSS.item()))
                training_loss = 0
                training_step_out = 0

            if i % 20000 == 0:                         # 迭代20000次保存一次模型
                if torch.distributed.get_rank() == 0:  # 在第一台机器的第一张卡上保存模型
                # if args.local_rank == 0:
                    model_path = os.path.join("../model", "model_" + str(epoch_item) + "_" + str(i) + ".pkl")
                    torch.save(model.module.state_dict(), model_path)







































