import json
import re
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
import os
from Mongo.GetOther import GetOther
from Mongo.GetDataFromDB import GetData
from Mongo.User import User
from timepredict.time_predict import time_predict
from Clocks.RunClocks import DNAAgePredictor
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
app = Flask(__name__)
CORS(app)
import rpy2.robjects as robjects



@app.route('/')
def hello_world():
    return 'Hello'

#按钮功能，负责接受数据并检测上传格式等
@app.route('/api/upload', methods=['POST', 'GET'])
def upload():
    print('________first working________')
    beta_file = request.files.get('beta')
    print(beta_file)
    pheno_file = request.files.get('pheno')
    beta_file_path = os.path.join("./data/beta/", beta_file.filename)
    pheno_file_path = os.path.join("./data/pheno/", pheno_file.filename)
    beta_file.save(beta_file_path)
    pheno_file.save(pheno_file_path)
    data = pd.read_csv(beta_file_path)
    ph = pd.read_csv(pheno_file_path)
    print(data.columns.tolist()[1])
    head_check = re.search('GSM', data.columns.tolist()[1])
    if (head_check == None):
        return 'BetaHeadErr'
    ios = ph['ID'].tolist()
    if ios.__len__() > 200:
        return 'TooMuchErr'
    for ioss in ios:
        if len(str(ioss)) < 4:
            return 'PhoneIdErr'
    phone_head_map = ['ID', 'Tissue']  # , 'Disease', 'Condition', 'Age', 'Age_unit', 'Gender', 'Race', 'Platform'
    for phone_head_one in phone_head_map:
        if not phone_head_one in ph.columns.tolist():
            return 'PhoneHeadErr'

    clocks = request.form.get('clocks').split(',')
    print(clocks)
    if ph['ID'].tolist() != data.columns.tolist()[1:]:
        return 'IDMismatch'
    # 实例化类
    file = "../data/beta/" + beta_file.filename
    # predictor = DNAAgePredictor(beta_file.filename, pheno_file.filename, fill_value=0.5)
    # age = predictor.predict_age(clocks)
    # task = GetOther()
    # print(task_info)
    # task.insert_task(task_info)
    beta_line_num = data[data.columns.tolist()[1]].tolist().__len__()
    phone_num = ios.__len__()
    print(time_predict(clocks, beta_line_num, phone_num))
    return str(round(time_predict(clocks, beta_line_num, phone_num),3))

#wait页面的功能，负责费事的数据处理
@app.route('/api/upload_back', methods=['POST', 'GET'])
def upload_back():
    print('___________second working___________')
    beta_file = request.files.get('beta')
    pheno_file = request.files.get('pheno')
    # 保存文件
    beta_file_path = os.path.join("./data/beta/", beta_file.filename)
    pheno_file_path = os.path.join("./data/pheno/", pheno_file.filename)
    beta_file.save(beta_file_path)
    pheno_file.save(pheno_file_path)
    data = pd.read_csv(beta_file_path, nrows=5)
    ph = pd.read_csv(pheno_file_path)
    clocks = request.form.get('clocks').split(',')
    print(clocks)
    if ph['ID'].tolist() != data.columns.tolist()[1:]:
        return 'IDMismatch'
    print(request.form.get('userName'))
    print(request.form.get('email'))
    task_info = {
        'task_id': request.form.get('taskID'),
        'user_name': request.form.get('userName'),
        'email': request.form.get('email'),
        'beta_data': beta_file.filename,
        'pheno_data': pheno_file.filename,
        'tissue': request.form.get('tissue'),
        'age_unit': request.form.get('ageUnit'),
        'imputation': request.form.get('imputation'),
        'clocks': clocks
    }
    # 实例化类
    file = "../data/beta/" + beta_file.filename
    predictor = DNAAgePredictor(beta_file.filename, pheno_file.filename, fill_value=0.5)
    age = predictor.predict_age(clocks)
    task = GetOther()
    print(task_info)
    task.insert_task(task_info)
    return 'success'

# 结果状态
@app.route('/api/resStatus', methods=['POST'])
def get_res_status():
    filename = request.form.get('files')
    print(filename)
    filenamelist = filename.split('_beta')
    f = open('Result/'+filenamelist[0]+'_predicted.json')
    print('Result/'+filenamelist[0]+'_predicted.json')
    data = json.load(f)
    print(data)
    return data


@app.route('/api/clocks', methods=['GET', 'POST'])
def get_clocks():
    clock = GetOther()
    clocks_list = clock.get_clocks()
    clock_data = {'data': clocks_list}
    return clock_data


@app.route('/api/getAgeUnits', methods=['GET', 'POST'])
def get_age_units():
    types = request.get_json(silent=True)
    print(types)
    return 'success'


# 登录
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email)
    print(password)
    user = User()
    res = user.get_user(email, password)
    print(res)
    if res is False:
        return 'error'
    return res


# 注册
@app.route('/api/register', methods=['GET', 'POST'])
def register():
    register_data = {
        'firstName': request.form.get('fname'),
        'lastName': request.form.get('lname'),
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'institution': request.form.get('institution'),
        'country': request.form.get('country'),
        'title': request.form.get('title'),
        'status': request.form.get('status')
    }
    print(register_data)
    user = User()
    res = user.add_user(register_data)
    print(res)
    return 'success'


# 验证邮箱
@app.route('/api/checkEmail', methods=['GET', 'POST'])
def check_email():
    email = request.form.get('email')
    print(email)
    user = User()
    if user.check(email):
        return 'success'
    else:
        return 'unsuccess'


# 修改密码
@app.route('/api/resetPsw', methods=['GET', 'POST'])
def reset_psw():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User()
    if user.update_psw(email, password):
        return 'success'
    else:
        return 'unsuccess'


# 获取数据集
@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    get_data = GetData()
    data = get_data.get_dataset_data()
    print(data)
    return {'data': data}


# 获取疾病、组织、种族
@app.route('/api/tissue', methods=['GET'])
def get_tissue():
    get_data = GetData()
    data = get_data.get_tissue_data()
    return {'data': data}


# 获取疾病、组织、种族
@app.route('/api/race', methods=['GET'])
def get_race():
    get_data = GetData()
    data = get_data.get_race_data()
    return {'data': data}


# 获取疾病、组织、种族
@app.route('/api/disease', methods=['GET'])
def get_disease():
    get_data = GetData()
    data = get_data.get_disease_data()
    return {'data': data}


@app.route('/api/email_che', methods=['POST'])
def email_che():
    print('worked')
    answer_mail = request.form.get('beta')
    print(answer_mail)
    print(request.form.get('email'))
    mail_host = "smtp.163.com"
    mail_user = "taomi208874@163.com"
    mail_pass = "VDNZXWOSIMGOWIVK"
    receivers = request.form.get('email')
    message = MIMEText('Thanks for using our web', 'plain', 'utf-8')
    subject = 'Your CAPTCHA: '+str(answer_mail)
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    return 'success'

@app.route('/api/email_send', methods=['POST'])
def email_send():
    print('answer:')
    print(request.form.get('email'))
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    # message = MIMEText('data are Accessible at http://47.99.71.176:8080/#/result', 'plain', 'utf-8')
    # message['Subject'] = "Your data have been analyzed"
    mail_host = "smtp.163.com"
    mail_user = "taomi208874@163.com"
    mail_pass = "VDNZXWOSIMGOWIVK"
    receivers = request.form.get('email')
    message = MIMEText('data are Accessible at http://47.99.71.176:8080/#/result', 'plain', 'utf-8')
    subject = 'Your data have been analyzed'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8808)
