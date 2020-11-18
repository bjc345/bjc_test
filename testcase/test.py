import jsonpath
import pytest

test_data=[{"case_id":"case1","linked_data":"","data":{"id":"2333"}},{"case_id":"case2","linked_data":"case1-$..code","data":{"id":"2333","code":"case1-$..code"}},{"case_id":"case3","linked_data":"case1-$..code,case2-$..code","data":{"id":"2333","case1_code":"case1-$..code","case2_code":"case2-$..code"}}]
response_dict={}
def save_result(case_id,response_result):
    response_dict[case_id]=response_result

def get_Linkeddata(str):
    data_list=str.split(",")
    mapping_dict={}

    for v in data_list:
        if "-" in v:
            key=v.split('-')[0]
            value=v.split('-')[1]
            mapping_dict[v]=jsonpath.jsonpath(response_dict[key],value)[0]
    return mapping_dict

@pytest.mark.parametrize("data_dict",test_data)
def test(data_dict):
        case_id=data_dict["case_id"]
        linked_data=data_dict["linked_data"]
        if linked_data:
            linke_dict=get_Linkeddata(linked_data)
            for k,v in data_dict["data"].items():
                if v in linke_dict.keys():
                    data_dict["data"][k]=linke_dict[v]
        data=data_dict["data"]
        print(data)
        assert 1
        code_result={"code":200}
        save_result(case_id,code_result)
        print(response_dict)

def test2():
    assert 1==1

if __name__=="__main__":
    pass

