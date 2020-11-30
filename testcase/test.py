# -*- coding: utf-8 -*-
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
            mylog.warning(f"用例id为{case_id}的用例执行完毕，开始存储用例直接list中")
            linkeddataUtil.LinkedUtil().save_result(case_id, res)
            mylog.warning(f"用例保存成功，对应的case_id为{case_id},对应的response_body为{res}")
            AssertUtil.AssertUtil().assert_code(*getCodeUtil.getCodeUtil.getcode_tuple(res,case_checkcode))
    @pytest.mark.parametrize("case_dict",another_case)
    def test_another(self,init,case_dict):
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
        case_header={"Content-Type":"application/json","x-zjaisino-auth-token":init}
        if case_lindeddata:
            linke_dict=linkeddataUtil.LinkedUtil.get_Linkeddata(case_lindeddata)
            finallydict=JsonHelper.decode(case_senddata)
            for k,v in finallydict.items():
                if v in linke_dict.keys():
                    finallydict[k]=linke_dict[v]
            case_senddata=JsonHelper.format_cn_res(finallydict)
        allure.dynamic.title(case_title)
        if not (case_isrun=="yes"):
            mylog.warning(f"用例编号为{case_id},用例标题为:[{case_title}的用例，因为是否执行状态的值为{case_isrun}],此次执行结果为skip")
            pytest.skip(f"用例的是否执行值为{case_isrun}")
        if (case_isputfile =="no") and  case_sendtype=="post":
            mylog.warning(f"开始测试数据,此次获取到的用例id为{case_id},获取到的请求体为{case_senddata}")
            res=RequestUtil.Request().post(case_url,json=JsonHelper.decode(case_senddata),headers=case_header)
            print(getCodeUtil.getCodeUtil.getcode_tuple(res,case_checkcode))
            mylog.warning(f"用例id为{case_id}的用例执行完毕，开始存储用例直接list中")
            linkeddataUtil.LinkedUtil().save_result(case_id, res)
            mylog.warning(f"用例保存成功，对应的case_id为{case_id},对应的response_body为{res}")
            AssertUtil.AssertUtil().assert_code(*getCodeUtil.getCodeUtil.getcode_tuple(res,case_checkcode))
        else:
            mylog.warning(f"开始测试数据,此次获取到的用例id为{case_id}")
            res = RequestUtil.Request().get(case_url, data=JsonHelper.decode(case_senddata))
            print(getCodeUtil.getCodeUtil.getcode_tuple(res, case_checkcode))
            mylog.warning(f"用例id为{case_id}的用例执行完毕，开始存储用例直接list中")
            linkeddataUtil.LinkedUtil().save_result(case_id, res)
            mylog.warning(f"用例保存成功，对应的case_id为{case_id},对应的response_body为{res}")
            AssertUtil.AssertUtil().assert_code(*getCodeUtil.getCodeUtil.getcode_tuple(res, case_checkcode))






if __name__=="__main__":
    l={'code': 200, 'body': {'retCode': '000000', 'retData': {'page': 1, 'records': [{'codeGoodsName': '培训费', 'createTime': 1606458661000, 'goodsId': 1, 'hostDepartment': '吧哈哈', 'id': 1042, 'issuer': '刘晶晶', 'offset': 0, 'page': 1, 'size': 10, 'trainAmount': 1.0, 'trainCode': '20201127000008', 'trainDuration': 11.0, 'trainLocation': '123123', 'trainName': '1', 'trainStatus': 0, 'trainTime': 1606443480000, 'updateName': 'admin', 'updateTime': 1606458661000, 'valid': 1}, {'codeGoodsName': '培训费', 'createTime': 1606456974000, 'goodsId': 1, 'hostDepartment': '吧哈哈', 'id': 1041, 'issuer': '刘晶晶', 'offset': 0, 'page': 1, 'size': 10, 'trainAmount': 1.0, 'trainCode': '20201127000007', 'trainDuration': 11.0, 'trainLocation': '123123', 'trainName': '1', 'trainStatus': 0, 'trainTime': 1606443480000, 'updateName': 'admin', 'updateTime': 1606456974000, 'valid': 1}, {'codeGoodsName': '培训费', 'createTime': 1606447653000, 'goodsId': 1, 'hostDepartment': '吧哈哈', 'id': 1040, 'issuer': '刘晶晶', 'offset': 0, 'page': 1, 'size': 10, 'trainAmount': 1.0, 'trainCode': '20201127000006', 'trainDuration': 11.0, 'trainLocation': '123123', 'trainName': '1', 'trainStatus': 0, 'trainTime': 1606443480000, 'updateName': 'admin', 'updateTime': 1606447653000, 'valid': 1}, {'codeGoodsName': '培训费', 'createTime': 1606447603000, 'goodsId': 1, 'hostDepartment': '吧哈哈', 'id': 1039, 'issuer': '刘晶晶', 'offset': 0, 'page': 1, 'size': 10, 'trainAmount': 1.0, 'trainCode': '20201127000005', 'trainDuration': 11.0, 'trainLocation': '123123', 'trainName': '1', 'trainStatus': 0, 'trainTime': 1606443480000, 'updateName': 'admin', 'updateTime': 1606447603000, 'valid': 1}, {'codeGoodsName': '培训费', 'createTime': 1606447555000, 'goodsId': 1, 'hostDepartment': '吧哈哈', 'id': 1038, 'issuer': '刘晶晶', 'offset': 0, 'page': 1, 'size': 10, 'trainAmount': 1.0, 'trainCode': '20201127000004', 'trainDuration': 11.0, 'trainLocation': '123123', 'trainName': '1', 'trainStatus': 0, 'trainTime': 1606443480000, 'updateName': 'admin', 'updateTime': 1606447555000, 'valid': 1}, {'codeGoodsName': '培训费', 'createTime': 1606447083000, 'goodsId': 1, 'hostDepartment': '吧哈哈', 'id': 1037, 'issuer': '刘晶晶', 'offset': 0, 'page': 1, 'size': 10, 'trainAmount': 1.0, 'trainCode': '20201127000003', 'trainDuration': 11.0, 'trainLocation': '123123', 'trainName': '1', 'trainStatus': 0, 'trainTime': 1606443480000, 'updateName': 'admin', 'updateTime': 1606447083000, 'valid': 1}, {'codeGoodsName': '培训费', 'createTime': 1606446993000, 'goodsId': 1, 'hostDepartment': '吧哈哈', 'id': 1036, 'issuer': '刘晶晶', 'offset': 0, 'page': 1, 'size': 10, 'trainAmount': 1.0, 'trainCode': '20201127000002', 'trainDuration': 11.0, 'trainLocation': '123123', 'trainName': '1', 'trainStatus': 0, 'trainTime': 1606443480000, 'updateName': 'admin', 'updateTime': 1606446993000, 'valid': 1}, {'codeGoodsName': '培训费', 'createTime': 1606445206000, 'goodsId': 1, 'hostDepartment': '吧哈哈', 'id': 1035, 'issuer': '刘晶晶', 'offset': 0, 'page': 1, 'size': 10, 'trainAmount': 1.0, 'trainCode': '20201127000001', 'trainDuration': 11.0, 'trainLocation': '123123', 'trainName': '1', 'trainStatus': 0, 'trainTime': 1606443480000, 'updateName': 'admin', 'updateTime': 1606445206000, 'valid': 1}, {'codeGoodsName': '培训费', 'createTime': 1603350815000, 'goodsId': 1, 'hostDepartment': '55225', 'id': 1034, 'issuer': '刘晶晶', 'offset': 0, 'page': 1, 'remark': '1111', 'size': 10, 'trainAmount': 1.0, 'trainCode': '20201022000001', 'trainDuration': 1.0, 'trainLocation': '123123', 'trainName': '123123123', 'trainStatus': 0, 'trainTime': 1603350720000, 'updateName': 'admin', 'updateTime': 1603780051000, 'valid': 1}, {'codeGoodsName': '培训费', 'createTime': 1603178157000, 'goodsId': 2, 'hostDepartment': '保健科', 'id': 1033, 'issuer': '黄珊珊', 'offset': 0, 'page': 1, 'remark': '222', 'size': 10, 'trainAmount': 0.01, 'trainCode': '20201020000002', 'trainDuration': 2.0, 'trainLocation': '333', 'trainName': '牙齿保健', 'trainStatus': 0, 'trainTime': 1603188900000, 'updateName': 'admin', 'updateTime': 1603178157000, 'valid': 1}], 'size': 10, 'totalItems': 1042, 'totalPages': 105}, 'retMsg': '', 'success': True}}
    print(jsonpath.jsonpath(l,"$..records[0].trainCode"))