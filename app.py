import json
import re
import signal
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
import multiprocessing
app = Flask(__name__)
CORS(app)
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import conversion, default_converter, pandas2ri
from rpy2.robjects.conversion import localconverter

with localconverter(default_converter + pandas2ri.converter):
    MEAT = importr("MEAT")
    table = importr("data.table")
    se = importr("SummarizedExperiment")
def get_res_by_taskID(taskIDs):
    reader = GetData()
    taskID = taskIDs
    databaselist = []
    adding = reader.get_taskIDS_predicted(taskID)
    for i in range(len(taskID)):
        databaselist.append(adding[i]['Dataset'])
    print(databaselist)
    datasetlist = list(set(databaselist))
    print(datasetlist)
    finalreturn = []
    event = 0
    for one_dataset in datasetlist:
        event = 0
        baseData = {}
        for i in range(len(taskID)):
            if adding[i]['Dataset'] == one_dataset:
                if event == 0:
                    baseData = adding[i]
                    event = 1
                else:
                    add_dict(baseData, adding[i])
        finalreturn.append(baseData)
        event = 0
    return finalreturn
def add_dict(dict_base,dict_addition):
    length = dict_base['SampleNum']
    meanless = 0
    for oneclock in dict_addition['PredAge'].keys():
        if oneclock in dict_base['PredAge'].keys():
            meanless = meanless+1
        else:
            dict_base['PredAge'][oneclock] = ['']*length
    for i in range(len(dict_addition['ID'])):
        if dict_addition['ID'][i] in dict_base['ID']:
            for onekey in dict_addition['PredAge'].keys():

                dict_base['PredAge'][onekey][dict_base['ID'].index(dict_addition['ID'][i])] = dict_addition['PredAge'][onekey][i]

        else:
            dict_base['ID'].append(dict_addition['ID'][i])
            dict_base['SampleNum'] = dict_base['SampleNum'] + 1
            dict_base['Gender'].append(dict_addition['Gender'][i])
            dict_base['Race'].append(dict_addition['Race'][i])
            dict_base['Tissue'].append(dict_addition['Tissue'][i])
            dict_base['Disease'].append(dict_addition['Disease'][i])
            dict_base['Condition'].append(dict_addition['Condition'][i])
            dict_base['TrueAge'].append(dict_addition['TrueAge'][i])
            basekeys = dict_base['PredAge'].keys()
            additionkeys = dict_addition['PredAge'].keys()
            for onekey in basekeys:
                if onekey in additionkeys:
                    dict_base['PredAge'][onekey].append(dict_addition['PredAge'][onekey][i])
                else:
                    dict_base['PredAge'][onekey].append('')
def predect_and_save(event,beta_filename,pheno_filename,input_clocks, taskID, userName, email, tissue, ageUnit, imputation):
    try:
        print('___________second working___________')
        # 保存文件
        event.set()
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
        age = predictor.predict_age(clocks,email,taskID)
        task = GetOther()
        print(task_info)
        task.insert_task(task_info)
        mail_host = "smtp.163.com"
        mail_user = "taomi208874@163.com"
        mail_pass = "VDNZXWOSIMGOWIVK"
        receivers = email
        message = MIMEText('data are Accessible', 'plain', 'utf-8')
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
    except MemoryError:
        return 'memoryout'
    except AttributeError:
        return 'errread'
    except BaseException:
        print('unknown error')
        return 'myunknownerror'



@app.route('/')
def hello_world():
    return 'Hello'

#按钮功能，负责接受数据并检测上传格式等
@app.route('/api/upload', methods=['POST', 'GET'])
def upload():
    try:
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
        print(ph.columns.tolist())
        phone_head_map = ['ID', 'Tissue', 'Disease', 'Condition', 'Age', 'Age_unit', 'Gender', 'Race', 'Platform']  # , 'Disease', 'Condition', 'Age', 'Age_unit', 'Gender', 'Race', 'Platform'
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
        return str(round(time_predict(clocks, beta_line_num, phone_num), 3))
    except BaseException:
        print('unknown error')
        return 'unknownerror'



#wait页面的功能，负责费事的数据处理
@app.route('/api/upload_back', methods=['POST', 'GET'])
def upload_back():
    print('task creating')
    beta_file = request.files.get('beta')
    pheno_file = request.files.get('pheno')
    beta_file_name = beta_file.filename
    pheno_file_name = pheno_file.filename
    myevent = multiprocessing.Event()
    user_process = multiprocessing.Process(target=predect_and_save, args=(myevent,
                                                                          beta_file_name, pheno_file_name,
                                                                          request.form.get('clocks').split(','),
                                                                          request.form.get('taskID'),
                                                                          request.form.get('userName'),
                                                                          request.form.get('email'),
                                                                          request.form.get('tissue'),
                                                                          request.form.get('ageUnit'),
                                                                          request.form.get('imputation')))
    user_process.start()
    myevent.wait()
    return 'success'


# 结果状态
@app.route('/api/resStatus', methods=['POST'])
def get_res_status():
    ID = request.form.get('taskID')
    reader = GetData()
    i = 1
    while i==1:
        if(reader.get_taskID_predicted(ID).__len__() != 0):
            i = 0
            anser = reader.get_taskID_predicted(ID)
    print(request.form.get('taskID'))
    print('res_working')
    if anser[0]['Status'] == 'MemoryOut':
        return 'memoryout'
    if anser[0]['Status'] == 'unknownerror':
        return 'myunknownerror'
    filename = request.form.get('files')
    print(filename)
    filenamelist = filename.split('_beta')
    f = open('Result/'+filenamelist[0]+'_predicted.json')
    print('Result/'+filenamelist[0]+'_predicted.json')
    data = json.load(f)
    print(data)
    key_list = data['PredAge'].keys()
    clock_list = list(key_list)
    clock_list_before = ['Horvath Clock', 'OriginalMethod', 'Skin&Blood Clock', 'Zhang Clock', 'PedBE', 'Hannum Clock',
                         'Weidner Clock', 'Lin Clock', 'FeSTwo', 'MEAT', 'AltumAge', 'PhenoAge', 'BNN', 'EPM',
                         'Cortical Clock', 'VidalBralo Clock']
    clock_list_dist = {'Horvath Clock': 'HorvathAge', 'OriginalMethod': 'OriginalMethod',
                       'Skin&Blood Clock': 'Skin&BloodClock', 'Zhang Clock': 'ZhangBlupredAge',
                       'Hannum Clock': 'HannumAge', 'Weidner Clock': 'WeidnerAge', 'Lin Clock': 'LinAge',
                       'FeSTwo': 'FeSTwo', 'MEAT': 'MEAT', 'AltumAge': 'AltumAge', 'PhenoAge': 'PhenoAge', 'BNN': 'BNN',
                       'EPM': 'EPM', 'Cortical Clock': 'CorticalClock', 'VidalBralo Clock': 'VidalBraloAge',
                       'PedBE': 'PedBE'}
    for clock_name in clock_list_before:
        if clock_name in clock_list:
            data['PredAge'][clock_list_dist[clock_name]] = data['PredAge'].pop(clock_name)
    print(data)
    return data


@app.route('/api/clocks', methods=['GET', 'POST'])
def get_clocks():
    clock = GetOther()
    clocks_list = clock.get_clocks()
    clock_data = {'data': clocks_list}
    return clock_data

# 关闭进程
@app.route('/api/killprocess', methods=['GET', 'POST'])
def killprocess():
    print('working')
    piduse = request.form.get('user_pid')
    print(piduse)
    return 'success'


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

@app.route('/api/userdatasetback', methods=['POST'])
def get_userdataset_back():
    print(request.form.get('selected'))
    taskIDs = request.form.get('selected').split(',')
    read_result = get_res_by_taskID(taskIDs)
    clock_list_before = ['Horvath Clock', 'OriginalMethod', 'Skin&Blood Clock', 'Zhang Clock', 'PedBE', 'Hannum Clock',
                         'Weidner Clock', 'Lin Clock', 'FeSTwo', 'MEAT', 'AltumAge', 'PhenoAge', 'BNN', 'EPM',
                         'Cortical Clock', 'VidalBralo Clock']
    clock_list_dist = {'Horvath Clock': 'HorvathAge', 'OriginalMethod': 'OriginalMethod',
                       'Skin&Blood Clock': 'Skin&BloodClock', 'Zhang Clock': 'ZhangBlupredAge',
                       'Hannum Clock': 'HannumAge', 'Weidner Clock': 'WeidnerAge', 'Lin Clock': 'LinAge',
                       'FeSTwo': 'FeSTwo', 'MEAT': 'MEAT', 'AltumAge': 'AltumAge', 'PhenoAge': 'PhenoAge', 'BNN': 'BNN',
                       'EPM': 'EPM', 'Cortical Clock': 'CorticalClock', 'VidalBralo Clock': 'VidalBraloAge',
                       'PedBE': 'PedBE'}
    for i in range(len(read_result)):
        if 'PredAge' in read_result[i]:
            key_list = read_result[i]['PredAge'].keys()
            clock_list = list(key_list)
            for clock_name in clock_list_before:
                if clock_name in clock_list:
                    read_result[i]['PredAge'][clock_list_dist[clock_name]] = read_result[i]['PredAge'].pop(clock_name)
    return {'data': read_result}

@app.route('/api/readdatasets', methods=['GET', 'POST'])
def read_datasets():
    frontd = request.form.get('selected')
    frontdata = frontd.split(',')
    print(frontdata)
    front = request.form.get('model')
    print(front)
    reader = GetData()
    return_list = []
    if front == 'datasets':
        for one_frontdata in frontdata:
            return_list.append(reader.get_dataset(one_frontdata)[0])
    if front == 'tissue':
        for one_frontdata in frontdata:
            return_list.append(reader.get_tissue(one_frontdata)[0])
    if front == 'disease':
        for one_frontdata in frontdata:
            return_list.append(reader.get_disease(one_frontdata)[0])
    if front == 'race':
        for one_frontdata in frontdata:
            return_list.append(reader.get_raceb(one_frontdata)[0])
    print(return_list)
    return {'data': return_list}

@app.route('/api/connectus', methods=['POST'])
def connectus():
    to_email = '840883302@qq.com'
    email = request.form.get('email')
    messagea = request.form.get('message')
    name = request.form.get('name')
    print(email)
    print(messagea)
    print(name)
    print('worked')
    answer_mail = request.form.get('beta')
    print(answer_mail)
    print(request.form.get('email'))
    mail_host = "smtp.163.com"
    mail_user = "taomi208874@163.com"
    mail_pass = "VDNZXWOSIMGOWIVK"
    receivers = to_email
    message = MIMEText(messagea+'\nEmail at:'+email, 'plain', 'utf-8')
    subject = str('Message from '+ name)
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    return 'success'
    return {'data': 'read_result'}

@app.route('/api/userdataset', methods=['POST'])
def get_userdataset():
    reader = GetData()
    read_result = reader.get_user_predicted(request.form.get('email'))
    clock_list_before = ['Horvath Clock', 'OriginalMethod', 'Skin&Blood Clock', 'Zhang Clock', 'PedBE', 'Hannum Clock',
                         'Weidner Clock', 'Lin Clock', 'FeSTwo', 'MEAT', 'AltumAge', 'PhenoAge', 'BNN', 'EPM',
                         'Cortical Clock', 'VidalBralo Clock']
    clock_list_dist = {'Horvath Clock': 'HorvathAge', 'OriginalMethod': 'OriginalMethod',
                       'Skin&Blood Clock': 'Skin&BloodClock', 'Zhang Clock': 'ZhangBlupredAge',
                       'Hannum Clock': 'HannumAge', 'Weidner Clock': 'WeidnerAge', 'Lin Clock': 'LinAge',
                       'FeSTwo': 'FeSTwo', 'MEAT': 'MEAT', 'AltumAge': 'AltumAge', 'PhenoAge': 'PhenoAge', 'BNN': 'BNN',
                       'EPM': 'EPM', 'Cortical Clock': 'CorticalClock', 'VidalBralo Clock': 'VidalBraloAge',
                       'PedBE': 'PedBE'}
    for i in range(len(read_result)):
        if 'PredAge' in read_result[i]:
            key_list = read_result[i]['PredAge'].keys()
            clock_list = list(key_list)
            for clock_name in clock_list_before:
                if clock_name in clock_list:
                    read_result[i]['PredAge'][clock_list_dist[clock_name]] = read_result[i]['PredAge'].pop(clock_name)
    # read_result.reverse()
    read_result = sorted(read_result, key=lambda x: x['datetime'])
    # read_result.reverse()
    return {'data': read_result}

# 获取数据集
@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    get_data = GetData()
    data = get_data.get_dataset_data()
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
    message = MIMEText('data are Accessible', 'plain', 'utf-8')
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
