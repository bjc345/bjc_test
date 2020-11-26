from utils.logUtil import mylog
from utils.JsonHelper import format_cn_res

class AssertUtil:
    def __init__(self):
        self.mylog=mylog('AssertUtil')
    def assert_code(self,code,expect_code):
        try:
            assert int(code)==int(expect_code)
            # return True
        except:
            self.mylog.error('code状态码错误,code is {},expect_code is{}'.format(code,expect_code))
            # raise
    def assert_body(self,body,expect_body):
        try:
            assert body==expect_body
            # return True
        except:
            self.mylog.error('body值错误,body is {},expect_body is{}'.format(body,expect_body))
            # raise
    def assert_in_body(self,body,expect_body):
        try:
            body=format_cn_res(body)
            assert expect_body in body
            # return True
        except:
            self.mylog.error('不包含body或者body错误,body is {},expect_body is{}'.format(body,expect_body))
