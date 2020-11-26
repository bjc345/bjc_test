import jsonpath

class getCodeUtil:
    @staticmethod
    def getcode_tuple(response_dict,data):
        get_func=data.split("==")[0]
        check_code=data.split("==")[1]
        ys_value=jsonpath.jsonpath(response_dict,get_func)
        return ys_value[0],int(check_code)

if __name__ == '__main__':
    print(getCodeUtil.getcode_tuple(response_dict={"code":200},data="$..code==200"))



