import jsonpath
import pytest
import conftest
from utils import linkeddataUtil,yamlUtil,logUtil,RequestUtil,JsonHelper,AssertUtil,getCodeUtil
from config import conf
import allure

testcase_file=conf.get_TestCase_config_file()
login_case=[i for i in yamlUtil.YamlReader(testcase_file).load() if i["是否需要token"]=="no"]
another_case=[i for i in yamlUtil.YamlReader(testcase_file).load() if i["是否需要token"]!="no"]
mylog=logUtil.mylog()
# test_data=[{"case_id":"case1","linked_data":"","data":{"id":"2333"}},{"case_id":"case2","linked_data":"case1-$..code","data":{"id":"2333","code":"case1-$..code"}},{"case_id":"case3","linked_data":"case1-$..code,case2-$..code","data":{"id":"2333","case1_code":"case1-$..code","case2_code":"case2-$..code"}}]
#
#
# @pytest.mark.parametrize("data_dict",test_data)
# def test(data_dict):
#         case_id=data_dict["case_id"]
#         linked_data=data_dict["linked_data"]
#         if linked_data:
#             linke_dict=linkeddataUtil.LinkedUtil.get_Linkeddata(linked_data)
#             for k,v in data_dict["data"].items():
#                 if v in linke_dict.keys():
#                     data_dict["data"][k]=linke_dict[v]
#         data=data_dict["data"]
#         print(data)
#         assert 1
#         code_result={"code":200}
#         linkeddataUtil.LinkedUtil.save_result(case_id,code_result)
#         print(linkeddataUtil.response_dict
#         )
class Test:
    @pytest.mark.parametrize("case_dict",login_case)
    def test_login(self,case_dict):
        case_id=case_dict["用例编号"]
        case_title=case_dict["用例标题"]
        case_url=conf.ConfigYaml().get_conf_url()+case_dict["接口地址"]
        case_sendtype=case_dict["请求方式"]
        case_putfilename=case_dict["文件对象的参数名"]
        case_putfilepath=case_dict["上传文件路径"]
        case_lindeddata=case_dict["依赖数据"]
        case_senddata=case_dict["请求数据"]
        case_checkcode=case_dict["code校验"]
        case_isrun=case_dict["是否执行"]
        case_isusetoken=case_dict["是否需要token"]
        case_isputfile=case_dict["是否需要上传文件"]
        allure.dynamic.title(case_title)
        if not (case_isrun=="yes"):
            mylog.warning(f"用例编号为{case_id},用例标题为:[{case_title}的用例，因为是否执行状态的值为{case_isrun}],此次执行结果为skip")
            pytest.skip(f"用例的是否执行值为{case_isrun}")
        if (case_isputfile =="no") and  case_sendtype=="post":
            mylog.warning(f"开始测试数据,此次获取到的用例id为{case_id}")
            res=RequestUtil.Request().post(case_url,json=JsonHelper.decode(case_senddata))
            print(getCodeUtil.getCodeUtil.getcode_tuple(res,case_checkcode))
            AssertUtil.AssertUtil().assert_code(*getCodeUtil.getCodeUtil.getcode_tuple(res,case_checkcode))
            mylog.warning(f"用例id为{case_id}的用例执行完毕，开始存储用例直接list中")
            linkeddataUtil.LinkedUtil().save_result(case_id,res)
            mylog.warning(f"用例保存成功，对应的case_id为{case_id},对应的response_body为{res}")




if __name__=="__main__":
    AssertUtil.AssertUtil().assert_code("1111","111123123")

