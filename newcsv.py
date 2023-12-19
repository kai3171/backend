# import pandas as pd
#
#
#
# # 指定输入和输出文件的路径
# input_file = 'data/beta/GSE20242_beta.csv'
# output_file = 'GSE20242_beta.csv'
#
# # 调用函数创建新的 CSV 文件
# import pandas as pd
#
#
# def create_new_csv(input_file, output_file, column_index, start_column, end_column):
#     # 读取原始 CSV 文件
#     df = pd.read_csv(input_file)
#
#     # 提取指定列和范围内的列数据
#     selected_columns = [column_index] + list(range(start_column, end_column + 1))
#     new_df = df.iloc[:, selected_columns]
#
#     # 将提取的数据保存到新的 CSV 文件
#     new_df.to_csv(output_file, index=False)
#
#
# # 指定输入和输出文件的路径、列索引和范围
# column_index = 1  # 指定要保留的列索引（从0开始计数）
# start_column = 14  # 指定范围的起始列（从0开始计数）
# end_column = 29  # 指定范围的结束列（从0开始计数）
#
# # 调用函数创建新的 CSV 文件
# create_new_csv(input_file, output_file, column_index, start_column, end_column)
import pandas as pd
from Mongo.GetOther import GetOther
from Mongo.GetDataFromDB import GetData
from Mongo.MongoBase import MongoDBBase
reader = MongoDBBase(host='127.0.0.1', port=27017, username='root', password='admin', db_name='dnam_clocks')
answer = reader.clumn_find('protectionResult',{ },{'Dataset': 1, 'datetime': 1, 'Status': 1 ,'taskID': 1})
print(answer)
disease = []
for index, item in enumerate(answer):
    item.pop('_id')
    item['id'] = index + 1
    disease.append(item)
    print(item)
print(disease)
