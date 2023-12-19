from Mongo.MongoBase import MongoDBBase
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import conversion, default_converter, pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.rinterface as rinterface
import multiprocessing
from Mongo.GetDataFromDB import GetData
from Mongo.User import User

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
                dict_base['PredAge'][onekey][i] = dict_addition['PredAge'][onekey][i]
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
    print(dict_base)
reader = GetData()
databaselist = []
# adding = reader.get_taskIDS_predicted(taskID)
# for i in range(len(taskID)):
#     databaselist.append(adding[i]['Dataset'])
# print(databaselist)
# datasetlist =  list(set(databaselist))
# print(datasetlist)
# finalreturn = []
# event = 0
# for one_dataset in datasetlist:
#     event = 0
#     baseData = {}
#     for i in range(len(taskID)):
#         if adding[i]['Dataset'] == one_dataset:
#             if event == 0:
#                 baseData = adding[i]
#                 event = 1
#             else:
#                 add_dict(baseData,adding[i])
#     finalreturn.append(baseData)
#     event = 0

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
taskID = ['1702169580','1702169755','1702170609']
for one in get_res_by_taskID(taskID):
    print(one)
