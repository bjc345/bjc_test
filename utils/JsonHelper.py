import demjson


def format_cn_res(data, indent=3):
    """json数据解析"""
    # return json.dumps(data, indent=indent).encode('utf-8').decode('unicode_escape')
    return demjson.encode(data, indent_amount=indent, compactly=False).encode('utf-8').decode('unicode_escape')