import pytest
import os
if __name__ == '__main__':
    pytest.main(["-s","aa.py", '--alluredir', 'report1'])
    os.system('allure generate report1/ -o  report1/html --clean')