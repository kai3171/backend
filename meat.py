import json
import os
import time

import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import conversion, default_converter, pandas2ri
from rpy2.robjects.conversion import localconverter
import pandas as pd


MEAT = importr('MEAT')
table = importr("data.table")
Summ = importr('SummarizedExperiment')
# with localconverter(default_converter + pandas2ri.converter):
#     MEAT = importr("MEAT")
#     table = importr("data.table")
#     se = importr("SummarizedExperiment")
robjects.r.source('R/14/MEAT.R')
# run R test function
beta_path = 'data/beta/GSE34257_beta.csv'
fill_value = 0.5
RTestFunction = robjects.r.MEAT(beta_path, fill_value)
print(RTestFunction)
