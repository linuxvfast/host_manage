import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
sys.path.append(BASE_DIR)
import configparser
import paramiko
import threading
from conf import settings

class Server(object):
    def __init__(self,host,port,username,password,cmd):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.cmd = cmd


    def batch_cmd(self):
        '''执行命令'''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(self.host,self.port,self.username,self.password)
        ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
        stdin, stdout, stderr = ssh.exec_command(self.cmd)

        res,err =stdout.read(),stderr.read()
        result = res if res else err
        print('\033[44;1m%s\033[0m'.center(30,'-')%self.host)
        print(result.decode())
        ssh.close()

    def batch_put(self):
        '''上传文件'''
        transport = paramiko.Transport((self.host,int(self.port)))
        transport.connect(username=self.username, password=self.password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        if self.cmd.split()[0].startswith('put'):
            # 将location.py 上传至服务器 /tmp/test.py
            sftp.put(self.cmd.split()[1],self.cmd.split()[2])
            print('\033[44;1m %s 上传 %s 成功\033[0m'%(self.username,self.cmd.split()[1]))
        elif self.cmd.split()[0].startswith('get'):
            # 将remove_path 下载到本地 local_path
            sftp.get(self.cmd.split()[1],self.cmd.split()[2])
            print('\033[44;1m %s 下载 %s 成功\033[0m' % (self.username, self.cmd.split()[1]))
        else:
            print('\033[41;1m command not exist!!!\033')
            return


        transport.close()

    def function_distribution(self):
        '''实现功能分发'''
        if self.cmd.startswith('put') or self.cmd.startswith('get'):
            self.batch_put()
        else:
            self.batch_cmd()

def interactive():
    '''用户交互'''
    exits_flags = False
    while not exits_flags:
        config = configparser.ConfigParser()
        config.read(settings.ACCOUNT_DIR)
        print('服务器分组'.center(30,'-'))
        for i in config['server-g']:  #获取分组
            print(i,config['server-g'][i])

        choice = input('>>').strip()   #选择显示分组信息
        if len(choice) == 0 :continue
        if choice == 'exit':break
        if choice == 'server1':
            host_list = config['server-g'][choice]
            # print(host_list)
            host = host_list.split(',')
            # print(host)

            for key in host:
                print(key,' ',config[key]['server'])

        if choice == 'server2':
            host_list = config['server-g'][choice]
            # print(host_list)
            host = host_list.split(',')
            # print(host)
            for key in host:
                print(key, ' ', config[key]['server'])

        # exits_flags = True
        while True:
            cmd = input('命令>>').strip()
            thread_list = []
            if cmd:
                for key in host_list.split(','):
                    host,port,username,password =config[key]['server'],config[key]['port'],config[key]['username'],\
                                                 config[key]['password']
                    func = Server(host,port,username,password,cmd)
                    t = threading.Thread(target=func.function_distribution)
                    t.start()
                    thread_list.append(t)

                for i in thread_list:
                    i.join()





# def run():
#     interactive()


if __name__ == '__main__':
    interactive()
    # d = Server('192.168.10.116',22,'vfast','123456','df')
    # d.batch_cmd()
