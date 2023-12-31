import json
import os
import time

import pandas as pd

from Python.FeSTwo.FeSTwo import FeSTwoTest

def FeSTwoAge(beta_path):
    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + GEOID + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)
    # FeSTwo
    start_t = time.time()
    print('================NO.09=====================')
    FeSTwoAge = FeSTwoTest(id)
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    ageData = {
        "FileName": GEOID + "_predicted_by_NO.09.json",
        "datetime": curTime,
        "Algorithm": "NO.09_FeSTwo",
        "Dataset": GEOID,
        "Age_unit": pheno_data['Age_unit'].tolist()[0],
        "AgeRange": [min(trueAge), max(trueAge)],
        "SampleNum": len(trueAge),
        "ConsumeTime(Sec)": str(round((end_t - start_t), 3)) + 's',
        "Tissue": pheno_data['Tissue'].tolist(),
        "Condition": pheno_data['Condition'].tolist(),
        "Disease": pheno_data['Disease'].tolist(),
        "Gender": pheno_data['Gender'].tolist(),
        "Race": pheno_data['Race'].tolist(),
        "ID_REF": pheno_data['ID'].tolist(),
        "PredAge": FeSTwoAge,
        "TrueAge": trueAge,
        "Platform": pheno_data['Platform'].tolist()[0]
    }
    file = '../Result/09/' + GEOID + "_predicted_by_NO.09.json"
    with open(file, 'w') as f:
        json.dump(ageData, f)
    f.close()