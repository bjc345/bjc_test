import pytest
from utils import yamlUtil
from config import conf
from utils import RequestUtil
import jsonpath
from utils import logUtil

log_conftest=logUtil.mylog
# 注册自定义参数 cmdopt 到配置对象
# def pytest_addoption(parser):
#     parser.addoption("--cmdopt", action="store",
#                      default="这个是默认值...",
#                      choices=['python', 'java', 'c++'],
#                      help="将命令行参数 ’--cmdopt' 添加到 pytest 配置中")
# # 从配置对象中读取自定义参数的值
# @pytest.fixture(scope="session")
# def cmdopt(request):
#     yield request.config.getoption("--cmdopt")
# # 将自定义参数的值打印出来
# @pytest.fixture(autouse=True)
# def fix_1(cmdopt):
#     print('\n --cmdopt的值：', cmdopt)
# @pytest.fixture(autouse=True)
# def fix_0(cmdopt):
#     print('pass')
# @pytest.fixture(autouse=True)
# def fix_3(cmdopt):
#     print('fail')



@pytest.fixture(scope="session")
def init():
    yaml_file=conf.get_config_file()
    log_conftest().info("初始化token")
    yamlUtil.YamlReader(yaml_file).dump("Authorization","")
    log_conftest().info("清除token完成")
    log_conftest().info("开始登录，获取token")
    TestAdminName = conf.ConfigYaml().get_TestAdminName()
    TestAdminPassWord = conf.ConfigYaml().get_TestAdminPassWord()
    logindata = {"username": TestAdminName, "password": TestAdminPassWord}
    login_url = conf.ConfigYaml().get_conf_url() + "adminLogin"
    r = RequestUtil.Request().post(url=login_url, json=logindata)
    log_conftest().info(f'获取成功,token为{jsonpath.jsonpath(r,"$..token")[0]}')
    log_conftest().info("替代测试token")
    yamlUtil.YamlReader(yaml_file).dump("Authorization",jsonpath.jsonpath(r,"$..token")[0])
    log_conftest().info("替代成功")
    yield conf.ConfigYaml().get_Testtoken()
    log_conftest().info("测试完成,清理token")
    yamlUtil.YamlReader(yaml_file).dump("Authorization", "")
    log_conftest().info("清除token完成")
if __name__ == '__main__':
    pass