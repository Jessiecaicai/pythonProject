from pandas.tests.tools.test_to_datetime import epochs
from scipy.io.arff.tests.test_arffread import data_path

import esm
import esmz
import torch.nn as nn
import torch
import os
from Train_esm1b_CleanJessie import param_esm1b
import numpy as np
from torch.utils.data import DataLoader
from torch.nn import DataParallel
import loadingData
import torch.nn as nn
import pytest


### 加载原esm1b模型参数 33层
### 随机初始化参数
args = param_esm1b.params_parser()
esm1b_alphabetAfter = esmz.data.Alphabet.from_architecture(args.arch)
model = esmz.model.ProteinBertModel(args, esm1b_alphabetAfter)

esm1b, alphabet = esm.pretrained.esm1b_t33_650M_UR50S()
# state_dict = torch.load(model)
# state_esm1b = state_dict['model_state_dict']
### 赋原1b模型参数
model.state_dict().update({k: v for k, v in esm1b.state_dict().items() if k in model.state_dict().keys()})  #k为参数名 v对应参数值

### 训练模型
### 保证初始化的模型相同
os.environ['CUDA_VISIBLE_DEVICES'] = '3'
def init_seeds(SEED=1):
    torch.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(SEED)
    torch.cuda.manual_seed_all(SEED)

### 对所有GPU上的loss求平均，打印输出
def reduce_loss(value, average=True):
    world_size = torch.distributed.get_world_size()
    if world_size < 2:
        return value

    with torch.no_grad():
        output_tensors = value.clone()
        torch.distributed.all_reduce(output_tensors)
        if average:
            output_tensors /= world_size
        return output_tensors

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == '__main__':

    ### 初始化参数
    epochs = 20000
    batch_size = 24
    learning_rate =5e-5
    Seed = 2022
    init_seeds(SEED=Seed)

    ### 加载训练参数
    data_path = '/home/guo/pythonProject/chenlei/protein_representation_learning/data/downstream'
    train_dataset = loadingData.dataset_1b.FluorescenceDataset(data_path, 'train')
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=False, drop_last=True, collate_fn=train_dataset.collate__fn)
    model = DataParallel(model)

    model = model.to(model)
    criterion = nn.CrossEntropyLoss(ignore_index=-1)
    optimizer = torch.optim.Adam(esm1b.parameters(), lr=learning_rate)

    esm1b.to(device)
    esm1b.train()
    for epoch_item in range(epochs):
        #train_loader.sampler.set_epoch(epoch_item)
        training_loss = 0
        training_step = 0
        training_step_out = 0
        for i, data in enumerate(train_loader):
            tokens, all_label_ids = data
            tokens,all_label_ids = tokens.cuda(),all_label_ids.cuda()

            results = esm1b(tokens, return_contacts=False)
            logits = results["logits"].cuda()

            loss = criterion(logits.contiguous().view(-1, len(esm1b_alphabetAfter.all_toks)),all_label_ids.contiguous().view(-1))
            training_loss += loss
            training_step += 1
            training_step_out += 1

            optimizer.zero_grad()
            #with amp.scale_loss(loss,optimizer) as scaled_loss:
                #scaled_loss.backward()
            loss.backward()
            optimizer.step()
            #print(loss)
            if training_step_out % 100 == 0:
                training_loss /= training_step_out
                print("Epoch: {}. \t Step: {} / {} finish. \t TrainingLoss: {}".format(epoch_item, training_step, len(train_loader), training_loss))

            if i % 20000 == 0:                         # 迭代20000次保存一次模型
                model_path = os.path.join("./", "model_" + str(epoch_item) + "_" + str(i) + ".pkl")
                torch.save(esm1b.state_dict(), model_path)


