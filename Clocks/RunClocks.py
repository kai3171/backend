import json
import os
import time

import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import conversion, default_converter, pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.rinterface as rinterface
import pandas as pd
from Mongo.GetDataFromDB import GetData
import multiprocessing

table = importr("data.table")


# def MEAT_multy(queue,beta_path_my,fill_value_my):
#     with localconverter(default_converter + pandas2ri.converter):
#         # rinterface.initr()
#         # robjects.r('graphics.off()')
#         # robjects.r('rm(list=ls())')
#         robjects.r.source('R/14/MEAT.R')
#         # run R test function
#         RTestFunction = robjects.r.MEAT(beta_path_my, fill_value_my)
#         queue.put(list(RTestFunction))

class DNAAgePredictor:
    MEAT_USING = multiprocessing.Event()
    def __init__(self, beta_name: str, pheno_name: str, fill_value: float = 0.5):
        self.MEAT_USING.set()
        self.beta_name = beta_name
        self.pheno_path = pheno_name
        self.beta_path = 'data/beta/' + beta_name
        self.pheno_path = 'data/pheno/' + pheno_name
        self.fill_value = fill_value
        self.clock_name_mapping = {
            'Horvath Clock': 'horvath_age', 'Skin&Blood Clock': 'skin_blood_age',
            'Zhang Clock': 'zhang_blup_age', 'Hannum Clock': 'hannum_age',
            'Weidner Clock': 'weidner_age', 'Lin Clock': 'lin_age', 'PedBE': 'pedBE_age',
            'FeSTwo': 'FesTwo_age', 'MEAT': 'MEAT_age', 'AltumAge': 'Altum_age',
            'PhenoAge': 'pheno_age', 'BNN': 'BNN_age', 'EPM': 'EPM_age', 'Cortical Clock': 'cortical_clock_age',
            'VidalBralo Clock': 'vidal_bralo_age', 'OriginalMethod': 'PerSE_age'
        }

    def horvath_age(self) -> list:
        """
        Description: NO.01 Horvath 353 CpG Clock
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        print(self.beta_path)
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/01/Horvath.R')
            # run R test function
            RTestFunction = robjects.r.Horvath(self.beta_path, self.fill_value)
            print(list(RTestFunction))
        return list(RTestFunction)

    def skin_blood_age(self) -> list:
        """
        Description: NO.02 Horvath Skin & Blood 391 CpG Clock
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        print("skinWorking")
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/02/DNAmAgeSkinClock.R')
            # run R test function
            RTestFunction = robjects.r.SkinBloodAge(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def zhang_blup_age(self) -> list:
        """
        Description: NO.03 Zhang blup Clock
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/03/ZhangAge.R')
            # run R test function
            RTestFunction = robjects.r.ZhangAge(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def hannum_age(self) -> list:
        """
        Description: NO.04 Hannum 71 CpG Clock
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/04/Hannum.R')
            # run R test function
            RTestFunction = robjects.r.Hannum(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def weidner_age(self) -> list:
        """
        Description: NO.05 Weidner 3 CpG Clock
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/05/WeidnerAge.R')
            # run R test function
            RTestFunction = robjects.r.WeidnerAge(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def lin_age(self) -> list:
        """
        Description: NO.06
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/06/LinAge.R')
            # run R test function
            RTestFunction = robjects.r.LinAge(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def pedBE_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/08/PedBE.R')
            # run R test function
            RTestFunction = robjects.r.PedBE(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def MEAT_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        # self.MEAT_USING.wait()
        # self.MEAT_USING.clear()
        # print('MEATWORKING')

        with localconverter(default_converter + pandas2ri.converter):
            # rinterface.initr()
            # robjects.r('graphics.off()')
            # robjects.r('rm(list=ls())')
            robjects.r.source('R/14/MEAT.R')
            # run R test function
            RTestFunction = robjects.r.MEAT(self.beta_path, self.fill_value)
        # self.MEAT_USING.set()
        return list(RTestFunction)

    def pheno_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/17/Levine.R')
            # run R test function
            RTestFunction = robjects.r.Levine(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def BNN_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """

        with localconverter(default_converter + pandas2ri.converter):
            methylclocks = importr('methylclock')
            robjects.r.source('R/19/BNNAge.R')
            # run R test function
            RTestFunction = robjects.r.BNNAge(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def cortical_clock_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/24/CorticalClock.R')
            # run R test function
            RTestFunction = robjects.r.CorticalClock(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def vidal_bralo_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source('R/27/VidalBraloAge.R')
            # run R test function
            RTestFunction = robjects.r.VidalBraloAge(self.beta_path, self.fill_value)
        return list(RTestFunction)

    def Altum_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        from Python.AltumAge.AltumAge import AltumAge
        methylation = pd.read_csv(self.beta_path)
        methylation.index = methylation[methylation.columns[0]]
        methylation = methylation[methylation.columns[1:]].T
        AA = AltumAge('Python/AltumAge/AltumAge.h5',
                      'Python/AltumAge/scaler.pkl',
                      'Python/AltumAge/multi_platform_cpgs.pkl')
        pred_age = AA.predict(methylation, self.fill_value)
        return pred_age.tolist()

    def EPM_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        from Python.EpigeneticPacemaker.EPM import EPM
        # X_test = pd.read_csv(file_path, compression='gzip')
        X_test = pd.read_csv(self.beta_path)
        X_test.index = X_test[X_test.columns[0]]
        X_test = X_test[X_test.columns[1:]].T

        # generate predicted ages sing the test data
        epm_cv = EPM('Python/EpigeneticPacemaker/EPM_model.pkl',
                     'Python/EpigeneticPacemaker/selected_cpg_sites_NO22.pickle')
        pred_age = epm_cv.predict(X_test, self.fill_value)

        return pred_age.tolist()

    def FesTwo_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        from Python.FeSTwo.FeSTwo import FeSTwo
        methylation = pd.read_csv(self.beta_path)
        methylation.index = methylation[methylation.columns[0]]
        methylation = methylation[methylation.columns[1:]].T
        # get feature vector
        FE = FeSTwo("Python/FeSTwo/FeSTwo_lr_Model.pkl",
                    "Python/FeSTwo/command_Combination_FesTwo_lr_raw_Square.pickle")
        fea_vector = FE.get_sqare_raw_vertor(methylation, self.fill_value)
        # get predicted ages
        pred_age = FE.predict(fea_vector)
        return pred_age.tolist()

    def PerSE_age(self) -> list:
        """
        Description:
        :return: A list containing the predicted DNA methylation ages of all samples
        """
        from Python.PerSEClock.PerSEClock import PerSE_Test

        return PerSE_Test(self.beta_path)

    def predict_age(self, clock_names: list, useremail, taskID) -> dict:
        try:
            age_predictions = {}
            for clock_name in clock_names:
                print(clock_name)
                function_name = self.clock_name_mapping[clock_name]
                if hasattr(self, function_name):
                    age_predictions[clock_name] = np.round(np.array(getattr(self, function_name)()), 2).tolist()
                else:
                    age_predictions[clock_name] = "Invalid function name"
            pheno_data = pd.read_csv(self.pheno_path)
            pheno_data.fillna('Unknown', inplace=True)
            trueAge = pheno_data['Age'].tolist()
            localTime = time.localtime()
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
            result_predictions = {"datetime": curTime,
                                  "ID": pheno_data['ID'].tolist(),
                                  "Dataset": self.beta_name.split('_')[0],
                                  "AgeRange": [min(trueAge), max(trueAge)],
                                  "Gender": pheno_data['Gender'].tolist() if 'Gender' in pheno_data.columns else [
                                                                                                                     'Unknown'] * len(
                                      pheno_data),
                                  "Race": pheno_data['Race'].tolist() if 'Race' in pheno_data.columns else [
                                                                                                               'Unknown'] * len(
                                      pheno_data),
                                  "Tissue": pheno_data['Tissue'].tolist() if 'Tissue' in pheno_data.columns else [
                                                                                                                     'Unknown'] * len(
                                      pheno_data),
                                  "Disease": pheno_data['Disease'].tolist() if 'Disease' in pheno_data.columns else [
                                                                                                                        'Unknown'] * len(
                                      pheno_data),
                                  "Condition": pheno_data[
                                      'Condition'].tolist() if 'Condition' in pheno_data.columns else ['Unknown'] * len(
                                      pheno_data),
                                  "SampleNum": len(trueAge),
                                  "PredAge": age_predictions,
                                  "TrueAge": trueAge
                                  }
            print(result_predictions)
            result_file_name = 'Result/' + self.beta_name.split('_')[0] + '_predicted.json'
            print(result_file_name)
            with open(result_file_name, 'w') as f:
                json.dump(result_predictions, f)
            f.close()
            inserter = GetData()
            result_predictions['email'] = useremail
            result_predictions['Status'] = 'complete'
            result_predictions['taskID'] = taskID
            inserter.insert_into_protectionResult(result_predictions)
            return age_predictions
        except MemoryError:
            localTime = time.localtime()
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
            result_predictions = {"datetime": curTime,
                                  "Dataset": self.beta_name.split('_')[0],
                                  }
            print(result_predictions)
            result_file_name = 'Result/' + self.beta_name.split('_')[0] + '_predicted.json'
            print(result_file_name)
            with open(result_file_name, 'w') as f:
                json.dump(result_predictions, f)
            f.close()
            inserter = GetData()
            result_predictions['email'] = useremail
            result_predictions['Status'] = 'MemoryOut'
            result_predictions['taskID'] = taskID
            inserter.insert_into_protectionResult(result_predictions)
            return {}
        except BaseException:
            localTime = time.localtime()
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
            result_predictions = {"datetime": curTime,
                                  "Dataset": self.beta_name.split('_')[0],
                                  }
            print(result_predictions)
            result_file_name = 'Result/' + self.beta_name.split('_')[0] + '_predicted.json'
            print(result_file_name)
            with open(result_file_name, 'w') as f:
                json.dump(result_predictions, f)
            f.close()
            inserter = GetData()
            result_predictions['email'] = useremail
            result_predictions['Status'] = 'unknownerror'
            result_predictions['taskID'] = taskID
            inserter.insert_into_protectionResult(result_predictions)
            return {}



if __name__ == '__main__':
    # runTest('WeidnerAge', 'GSE20242_beta.csv', 'GSE20242_  pheno.csv')
    beta_name = 'GSE20242_beta.csv'
    pheno_name = 'GSE20242_pheno.csv'

    # 实例化类
    predictor = DNAAgePredictor(beta_name, pheno_name, fill_value=0.5)
    age = predictor.predict_age(['WeidnerAge'])
    print(age)

