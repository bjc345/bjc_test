#encoding=utf8
from ruamel     import yaml
import os



class YamlReader:
    def __init__(self,yamlf):
        if os.path.exists(yamlf):
            self.yamlf=yamlf
        else:
            raise Exception('文件不存在')
        self._data=None

    def load(self):
        if self._data:
            return self._data
        with open(self.yamlf, encoding='utf8') as f:
            s = yaml.safe_load(f)
            return s

    def load_all(self):
        if self._data:
            return self._data
        with open(self.yamlf, encoding='utf8') as f:
            s = yaml.safe_load_all(f)
            return [i for i in s]

    def dump(self,key,value):
            s=self.load()
            s['BASE']['test'][key]=value
            with open(self.yamlf,encoding='utf8',mode='w') as f:
                result=yaml.dump(s,Dumper=yaml.RoundTripDumper)
                f.write(result)
    def dump_dict_or_list(self,dict_or_list):
        with open(self.yamlf,encoding='utf8',mode='w') as f:
            yaml.dump(dict_or_list,f,Dumper=yaml.RoundTripDumper)


















