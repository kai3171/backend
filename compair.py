from Mongo.MongoBase import MongoDBBase


class GetData:
    def __init__(self):
        self.mongo = MongoDBBase(host='127.0.0.1', port=27017, username='root', password='admin', db_name='dnam_clocks')

    def get_dataset_data(self):
        """
        获取数据集结果数据
        :return: 数据集结果数据
        """
        datasets = []
        # 查找
        result = self.mongo.clumn_find('datasets', {},{'Dataset': 1 ,'AgeRange': 1 ,'Age_unit': 1 ,'SampleNum': 1})
        # result = self.mongo.find('datasets', {})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_table_data(self, table):
        datasets = []
        result = self.mongo.find(table,{})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_dataset(self, dataset):
        datasets = []
        result = self.mongo.find('datasets',{'Dataset': dataset})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_taskID_predicted(self, ID):
        datasets = []
        result = self.mongo.find('protectionResult',{'taskID': ID})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets

    def get_user_predicted(self, email):
        datasets = []
        # result = self.mongo.find('protectionResult',{'email': email})
        result = self.mongo.clumn_find('protectionResult', {'email': email},{'Dataset': 1, 'datetime': 1, 'Status': 1 ,'taskID': 1 ,'AgeRange': 1, 'SampleNum': 1, 'PredAge': 1})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets

    def get_taskIDS_predicted(self, taskIDs):
        datasets = []
        for taskID in taskIDs:
            result = self.mongo.find('protectionResult', {'taskID': taskID})
            for index, item in enumerate(result):
                item.pop('_id')
                item['id'] = index + 1
                datasets.append(item)
        return datasets

    def get_tissue(self, dataset):
        datasets = []
        result = self.mongo.array_find('tissues','Tissue',dataset)
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_disease(self, dataset):
        print('disease')
        datasets = []
        result = self.mongo.array_find('diseases','Disease',dataset)
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets

    def get_raceb(self, dataset):
        print('race working')
        datasets = []
        result = self.mongo.array_find('races','Race',dataset)
        print(result)
        for index, item in enumerate(result):
            print(item)
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_race(self, dataset):
        datasets = []
        result = self.mongo.find('races',{'Dataset': dataset})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets

    def get_disease_data(self):
        """
        获取疾病结果数据
        :return: 疾病结果数据
        """
        disease = []
        # 查找
        result = self.mongo.clumn_find('diseases', {},{'Disease': 1,'SampleNum': 1})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            item['Diseases'] = item['Disease'][0]
            disease.append(item)
        return disease

    def get_race_data(self):
        """
        获取种族结果数据
        :return: 种族结果数据
        """
        race = []
        # 查找
        result = self.mongo.clumn_find('races', {},{'Race': 1, 'SampleNum': 1})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            item['Races'] = item['Race'][0]
            race.append(item)
        return race


    def get_tissue_data(self):
        """
        获取组织结果数据
        :return: 组织结果数据
        """
        tissues = []
        # 查找
        result = self.mongo.clumn_find('tissues', {}, {'Tissue': 1,'SampleNum': 1})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            item['Tissues'] = item['Tissue'][0]
            tissues.append(item)
        return tissues

    def insert_into_protectionResult(self, value):
        """
        获取组织结果数据
        :return: 组织结果数据
        """
        # 查找
        self.mongo.insert_one('protectionResult',value)

        return 'success'
class GetDataB:
    def __init__(self):
        self.mongo = MongoDBBase(host='127.0.0.1', port=27017, username='root', password='admin', db_name='dnam_clocks_second')

    def get_dataset_data(self):
        """
        获取数据集结果数据
        :return: 数据集结果数据
        """
        datasets = []
        # 查找
        result = self.mongo.clumn_find('datasets', {},{'Dataset': 1 ,'AgeRange': 1 ,'Age_unit': 1 ,'SampleNum': 1})
        # result = self.mongo.find('datasets', {})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_table_data(self, table):
        datasets = []
        result = self.mongo.find(table,{})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_dataset(self, dataset):
        datasets = []
        result = self.mongo.find('datasets',{'Dataset': dataset})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_taskID_predicted(self, ID):
        datasets = []
        result = self.mongo.find('protectionResult',{'taskID': ID})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets

    def get_user_predicted(self, email):
        datasets = []
        # result = self.mongo.find('protectionResult',{'email': email})
        result = self.mongo.clumn_find('protectionResult', {'email': email},{'Dataset': 1, 'datetime': 1, 'Status': 1 ,'taskID': 1 ,'AgeRange': 1, 'SampleNum': 1, 'PredAge': 1})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets

    def get_taskIDS_predicted(self, taskIDs):
        datasets = []
        for taskID in taskIDs:
            result = self.mongo.find('protectionResult', {'taskID': taskID})
            for index, item in enumerate(result):
                item.pop('_id')
                item['id'] = index + 1
                datasets.append(item)
        return datasets

    def get_tissue(self, dataset):
        datasets = []
        result = self.mongo.array_find('tissues','Tissue',dataset)
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_disease(self, dataset):
        print('disease')
        datasets = []
        result = self.mongo.array_find('diseases','Disease',dataset)
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets

    def get_raceb(self, dataset):
        print('race working')
        datasets = []
        result = self.mongo.array_find('races','Race',dataset)
        print(result)
        for index, item in enumerate(result):
            print(item)
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets
    def get_race(self, dataset):
        datasets = []
        result = self.mongo.find('races',{'Dataset': dataset})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets

    def get_disease_data(self):
        """
        获取疾病结果数据
        :return: 疾病结果数据
        """
        disease = []
        # 查找
        result = self.mongo.clumn_find('diseases', {},{'Disease': 1,'SampleNum': 1})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            item['Diseases'] = item['Disease'][0]
            disease.append(item)
        return disease

    def get_race_data(self):
        """
        获取种族结果数据
        :return: 种族结果数据
        """
        race = []
        # 查找
        result = self.mongo.clumn_find('races', {},{'Race': 1, 'SampleNum': 1})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            item['Races'] = item['Race'][0]
            race.append(item)
        return race


    def get_tissue_data(self):
        """
        获取组织结果数据
        :return: 组织结果数据
        """
        tissues = []
        # 查找
        result = self.mongo.clumn_find('tissues', {}, {'Tissue': 1,'SampleNum': 1})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            item['Tissues'] = item['Tissue'][0]
            tissues.append(item)
        return tissues

    def insert_into_protectionResult(self, value):
        """
        获取组织结果数据
        :return: 组织结果数据
        """
        # 查找
        self.mongo.insert_one('protectionResult',value)

        return 'success'


if __name__ == '__main__':
    reader = GetData()
    readerb = GetDataB()
    clocksa = reader.get_table_data('clocks')
    clocksb = readerb.get_table_data('clocks')
    print(clocksa == clocksb)
    clocksa = reader.get_table_data('datasets')
    clocksb = readerb.get_table_data('datasets')
    print(clocksa == clocksb)
    clocksa = reader.get_table_data('diseases')
    clocksb = readerb.get_table_data('diseases')
    print(clocksa == clocksb)
    clocksa = reader.get_table_data('protectionResult')
    clocksb = readerb.get_table_data('protectionResult')
    print(clocksa == clocksb)
    clocksa = reader.get_table_data('races')
    clocksb = readerb.get_table_data('races')
    print(clocksa == clocksb)
    clocksa = reader.get_table_data('tasks')
    clocksb = readerb.get_table_data('tasks')
    print(clocksa == clocksb)
    clocksa = reader.get_table_data('tissues')
    clocksb = readerb.get_table_data('tissues')
    print(clocksa == clocksb)
    clocksa = reader.get_table_data('users')
    clocksb = readerb.get_table_data('users')
    print(clocksa == clocksb)


