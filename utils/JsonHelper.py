import demjson


def format_cn_res(data, indent=3):
    """json数据解析"""
    # return json.dumps(data, indent=indent).encode('utf-8').decode('unicode_escape')
    return demjson.encode(data, indent_amount=indent, compactly=False).encode('utf-8').decode('unicode_escape')

def decode(data):
    return demjson.decode(data)


if __name__=="__main__":
    a=decode('{"goodsId":11,"issuer":"刘艳映","codeGoodsName": "015培训费","trainCode":"case_6-$..records[0].trainCode","trainName":"发挥中医护理特色","hostDepartment":"护理一科","trainLocation":"护理二楼201室","trainTime":1588129705000,"trainDuration":2,"trainStatus":0,"trainAmount":10000.00,"remark": "备注"}')
    print(a)