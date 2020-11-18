import  logging
import config.conf
import datetime
import os

logging_dict={
    "info":logging.INFO,
    "debug":logging.DEBUG,
    "warning":logging.WARNING,
    "error":logging.ERROR
}
s=config.conf.get_log_path()
s1=config.conf.ConfigYaml().get_log_extention()
current_time=datetime.datetime.now().strftime("%Y-%m-%d")
s2=current_time+s1

log_file=os.path.join(s,s2)


log_level=config.conf.ConfigYaml().get_log_level()
class Logger:

    def __init__(self,log_file,log_name,log_level):

        self.log_file=log_file
        self.log_name=log_name
        self.log_level=log_level
        self.logger=logging.getLogger(self.log_name)
        self.logger.setLevel(logging_dict[self.log_level])
        if not self.logger.handlers:
            fh_stream=logging.StreamHandler()
            fh_stream.setLevel(logging_dict[self.log_level])
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y%m%d-%H:%M:%S")
            fh_file=logging.FileHandler(self.log_file,encoding='utf-8')
            fh_file.setLevel(logging_dict[self.log_level])
            fh_stream.setFormatter(formatter)
            fh_file.setFormatter(formatter)
            self.logger.addHandler(fh_file)
            self.logger.addHandler(fh_stream)




def mylog(log_name=__file__):
    return Logger(log_file=log_file,log_level=log_level,log_name=log_name).logger


if __name__=="__main__":
    mylog().debug('1111111111')
