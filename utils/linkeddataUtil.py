import jsonpath

response_dict={}
class LinkedUtil:
    @staticmethod
    def save_result(case_id, response_result):
        response_dict[case_id] = response_result

    @staticmethod
    def get_Linkeddata(str):
        data_list = str.split(",")
        mapping_dict = {}

        for v in data_list:
            if "-" in v:
                key = v.split('-')[0]
                value = v.split('-')[1]
                mapping_dict[v] = jsonpath.jsonpath(response_dict[key], value)[0]
        return mapping_dict