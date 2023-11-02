import pandas as pd
from rpy2.robjects import conversion, default_converter, pandas2ri
from rpy2.robjects.conversion import localconverter
pandas2ri.activate()

dataFrame = pd.DataFrame(data)
with localconverter(default_converter + pandas2ri.converter):
    dataFrameR = conversion.py2rpy(dataFrame)
robjects.globalenv['dataFrameR'] = dataFrameR
with localconverter(default_converter + pandas2ri.converter):
	conversion.rpy2py(robjects.r(r_script))
	result = conversion.rpy2py(robjects.r('result'))
