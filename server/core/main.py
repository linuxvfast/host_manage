import configparser
import paramiko
import threading
from conf import settings

class Server(object):
    pass

    def interactive(self):
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

def run():
    d = Server()
    d.interactive()