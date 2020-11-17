import pytest
import yaml
import datetime,timedelta,os
with open('test.yaml',mode='r',encoding='utf-8') as f:
    s=yaml.safe_load(f)

fw=['yunwei']


class Test1:

    @pytest.mark.flaky(reruns=5,reruns_delay=2)
    @pytest.mark.parametrize('data',s)
    def test_a(self,data):
        if data['所属模块'] not in fw:
            pytest.skip(f'不在此次运行范围中,此次用例模块运行范围为{fw},当前用例模块为{data["所属模块"]}')
        assert 1==2

    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_c(self):
        assert 2==1

if __name__ == '__main__':
    pass
    pytest.main(['test_a.py::Test1::test_a','-sv','--alluredir','report1'])
    os.system('allure generate report1/ -o  report1/html --clean')