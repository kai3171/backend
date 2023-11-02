import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
#画图
import matplotlib.pyplot as plt #导入matplotlib模块，并简写成plt
from scipy import optimize
import scipy.stats as stats

cpg_path = "Python/PerSEClock/24516cpg.csv"
cpg = pd.read_csv(cpg_path)
# print(cpg)
# cpg = cpg["cpg"]
# print('-------------------------分割---------------------')
# print(cpg)
# cpg_list = cpg.tolist()
file_beta_path = 'data/beta/GSE23638_beta.csv'
check_features = pd.read_csv(file_beta_path)
check_features = check_features.T  # 转置
data_featuresF = check_features.loc[:, cpg]

