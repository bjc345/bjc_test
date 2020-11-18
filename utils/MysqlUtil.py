import pymysql
import pandas
from  config import conf


class Mysql:
    def __init__(self,host,user,password,db_name,port,charset='utf8'):
        self.con=pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db_name,
            charset=charset,
            port=port
        )
    def read_sql(self,sql):
        return pandas.read_sql(con=self.con,sql=sql).values.tolist()

if __name__=="__main__":
    s=conf.ConfigYaml()

    s=Mysql(host=s.get_db_host(),user=s.get_db_user(),password=s.get_db_password(),db_name=s.get_db_name(),charset=s.get_db_charset(),port=s.get_db_port())

    l=s.read_sql("select * from notice_config")
    print(l)


