import pytest
import os
import config
from config import conf
from utils import yamlUtil,ExcelUtil

allure_data=conf.ConfigYaml().get_report_data()
allure_html=conf.ConfigYaml().get_report_html()
test_case_yaml=conf.get_TestCase_config_file()
case_dict=ExcelUtil.ExcelReader('./case_new.xlsx',0).data()

def main():
    yamlUtil.YamlReader(test_case_yaml).dump_dict_or_list(case_dict)

if __name__ == '__main__':
    # import sys
    #
    # for i in sys.path:
    #     print(i)
    main()
    pytest.main([])

    os.system(f'allure generate {allure_data}/ -o  {allure_html} --clean')