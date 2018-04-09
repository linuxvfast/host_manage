import configparser
import paramiko
import threading
from conf import settings

class Server(object):
    def batch_cmd(self,user_list):
        '''执行命令'''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=user_list[ip])

    def batch_put(self,user_list):
        '''上传文件'''
        pass

    def interactive(self):
        '''用户交互'''
        config = configparser.ConfigParser()
        config.read(settings.ACCOUNT_DIR)
        print('group1\t2台\ngroup2\t1台')
        while True:
            choice = input('>>').strip()
            if len(choice) == 0 :continue
            if choice == 'exit':break
            if choice == 'group1':
                for key in config[choice]:
                    if key == 'ip' or key == 'ip1':
                        print(key,' ',config[choice][key])
            elif choice == 'group2':
                for key in config[choice]:
                    if key == 'ip' or key == 'ip1':
                        print(key,' ',config[choice][key])
            else:
                print('\033[41;1m输入错误,请重新输入！\033[0m')
            while True:
                print('可执行的操作'.center(30,'-'))
                print('1\t执行命令\n2\t上传文件')
                choice_option = input('>>>').strip()
                if choice_option == '1':
                    self.batch_cmd(config[choice])
                elif choice_option == '2':
                    self.batch_put(config[choice])
                else:
                    continue


def run():
    d = Server()
    d.interactive()
    d.user_operation()