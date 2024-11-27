import json
import os


class ReadJsonFileUtils:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.get_data()

    def get_data(self):
        fp = open(self.file_name, encoding='utf-8')
        data = json.load(fp)
        fp.close()
        return data

    def get_value(self, id):
        return self.data[id]

    @staticmethod
    def get_data_path(folder, fileName):
        BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_file_path = os.path.join(BASE_PATH, folder, fileName)
        return data_file_path


if __name__ == '__main__':
    opers = ReadJsonFileUtils("..\\resources\\test_http_post_data.json")
    # 读取文件中的dataItem,是一个list列表，list列表中包含多个字典
    dataitem = opers.get_value('dataItem')
    print(dataitem)
