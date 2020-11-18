import  requests
from config.conf import *
from utils.yamlUtil import YamlReader
class Request:
    def requests_api(self,url,json=None,method='get',data=None,headers=None,**kwargs):
        if method=='get':
            r=requests.get(url=url,data=data,headers=headers,**kwargs)
        elif method=="post":
            r=requests.post(url=url,json=json,headers=headers,**kwargs)


        code=r.status_code

        body=r.json()

        body=r.text
        res=dict()
        res['code']=code
        res['body']=body
        return res
    def get(self,url,**kwargs):
        return self.requests_api(url=url,method='get',**kwargs)

    def post(self,url,json=None,**kwargs):
        return self.requests_api(url=url,method='post',json=json,**kwargs)



if __name__=="__main__":
    pass
    # url=ConfigYaml().get_conf_url()+'login'
    # data={"accountNumber":"aisino","password":"aisino123"}
    #
    # s=Request().requests_api(url=url,json=data,method='post')
