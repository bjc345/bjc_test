import pytest
import os
from config import conf
allure_data=conf.ConfigYaml().get_report_data()
allure_html=conf.ConfigYaml().get_report_html()
if __name__ == '__main__':
    pytest.main([])
    os.system(f'allure generate {allure_data}/ -o  {allure_html} --clean')