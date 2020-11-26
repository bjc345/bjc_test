from utils.yamlUtil import YamlReader
from pathlib import *
import os


BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf_path=BASE_DIR+os.sep+'config'

log_path=BASE_DIR+os.sep+'logs'

report_path=BASE_DIR+os.sep+"report"




#定义测试数据yaml地址
TestCase_file=conf_path+os.sep+'TestCase_conf.yaml'

#定义测试报告yaml地址
TestCaseReport_file=conf_path+os.sep+'Report_conf.yaml'

#定义yaml路径
conf_file=conf_path+os.sep+'conf.yaml'


#定义数据库yaml地址
db_conf_file=conf_path+os.sep+'db_conf.yaml'


def get_config_path():
    return conf_path

def get_config_file():
    return conf_file
def get_db_config_file():
    return db_conf_file
def get_TestCase_config_file():
    return TestCase_file
def get_log_path():
    return log_path

def get_report_config_file():
    return TestCaseReport_file



class ConfigYaml:
    def __init__(self):
        self.config=YamlReader(get_config_file()).load()
        self.config_db=YamlReader(get_db_config_file()).load()
        self.config_TestCase=YamlReader(get_TestCase_config_file()).load()
        self.config_TestCaseReport=YamlReader(get_report_config_file()).load()
    def get_conf_url(self):
        return self.config['BASE']['test']['url']

    def get_log_level(self):
        return self.config['BASE']['log_level']

    def get_log_extention(self):
        return self.config['BASE']['log_extension']
    def get_TestAdminName(self):
        return self.config['BASE']['test']['AdminName']
    def get_TestAdminPassWord(self):
        return self.config['BASE']['test']['AdminPassWord']
    def get_Testtoken(self):
        return self.config['BASE']['test']['Authorization']



   #数据库操作
    def get_db_host(self):
        return self.config_db['db1']['host']

    def get_db_user(self):
        return self.config_db['db1']['user']
    def get_db_name(self):
        return self.config_db['db1']['db_name']

    def get_db_password(self):
        return self.config_db['db1']['password']
    def get_db_charset(self):
        return self.config_db['db1']['charset']

    def get_db_port(self):
        return self.config_db['db1']['port']

    #测试用例读取

    #获取测试报告data
    def get_report_data(self):
        return self.config_TestCaseReport["filepath"]["data_path"]
    def get_report_html(self):
        return self.config_TestCaseReport['filepath']['report_path']
if __name__=="__main__":
    print(ConfigYaml().get_TestAdminName(),ConfigYaml().get_TestAdminPassWord())


