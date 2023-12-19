
import json
import re
import signal
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
import os
import multiprocessing
from Mongo.GetOther import GetOther
from Mongo.GetDataFromDB import GetData
from Mongo.User import User
from timepredict.time_predict import time_predict
from Clocks.RunClocks import DNAAgePredictor
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import conversion, default_converter, pandas2ri
from rpy2.robjects.conversion import localconverter
import multiprocessing

print('___________second working___________')
# 保存文件
beta_file_path = 'data/beta/GSE20242_beta.csv'
pheno_file_path = 'data/pheno/GSE20242_pheno.csv'
data = pd.read_csv(beta_file_path, nrows=5)
ph = pd.read_csv(pheno_file_path)
clocks =['Skin&Blood Clock'] #, 'Zhang Clock', 'Hannum Clock', 'Weidner Clock', 'Lin Clock', 'PedBE', 'FeSTwo', 'MEAT', 'AltumAge', 'PhenoAge', 'BNN', 'EPM', 'Cortical Clock', 'VidalBralo Clock'
print(clocks)

# 实例化类
predictor = DNAAgePredictor('GSE20242_beta.csv', 'GSE20242_pheno.csv', fill_value=0.5)
age = predictor.predict_age(clocks)
def predect_and_save(beta_filename,pheno_filename,input_clocks, taskID, userName, email, tissue, ageUnit, imputation):
    try:
        print('___________second working___________')
        # 保存文件
        beta_file_path = os.path.join("./data/beta/", beta_filename)
        pheno_file_path = os.path.join("./data/pheno/", pheno_filename)
        data = pd.read_csv(beta_file_path, nrows=5)
        ph = pd.read_csv(pheno_file_path)
        clocks = input_clocks
        print(clocks)
        task_info = {
            'task_id': taskID,
            'user_name': userName,
            'email': email,
            'beta_data': beta_filename,
            'pheno_data': pheno_filename,
            'tissue': tissue,
            'age_unit': ageUnit,
            'imputation': imputation,
            'clocks': clocks
        }
        # 实例化类
        file = "../data/beta/" + beta_filename
        predictor = DNAAgePredictor(beta_filename, pheno_filename, fill_value=0.5)
        age = predictor.predict_age(clocks)
        task = GetOther()
        print(task_info)
        task.insert_task(task_info)
        return 'success'
    except MemoryError:
        return 'memoryout'
    except AttributeError:
        return 'errread'
    except BaseException:
        print('unknown error')
        return 'myunknownerror'



process_1 = multiprocessing.Process(target=predect_and_save, args=(beta_file_path,pheno_file_path,clocks,'nothing','liyunkai','840883302@qq.com','nothing','nothing','nothing'))
