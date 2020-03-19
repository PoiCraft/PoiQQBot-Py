import socket
import subprocess
import threading
import config

# 管道开服
run = subprocess.Popen(config.BEDROCKSERVEREXE,
                       stderr=subprocess.PIPE,
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       shell=True,
                       universal_newlines=True)


#   打印在屏幕上营造出一个控制台的假象
def OutputStartInfo():
    while True:
        OutputStartInfo = run.stdout.readline().strip()
        if None != OutputStartInfo:
            print(OutputStartInfo)


def ListenConsoleCommand():
    while True:
        command = input("> ")
        run.stdin.write('{0}\n'.format(command))
        run.stdin.flush()


threading.Thread(target=OutputStartInfo).start()
threading.Thread(target=ListenConsoleCommand).start()

while True:
    try:
        # 接收客户端连接
        s = socket.socket()
        s.bind(('127.0.0.1', 30000))
        s.listen(5)
        print('等待连接....')
        client, address = s.accept()
        print('连接成功')
        while True:
            try:
                try:
                    msg = client.recv(1024)
                except:
                    break
                if msg == b'EOF':
                    client.close()
                    break
                if msg == b'quit':
                    client.close()
                    break
                if msg == b'':
                    client.close()
                    break
                print('服务端接收并尝试执行:', msg.decode('utf-8'))
                run.stdin.write(str(msg, encoding=('utf-8')) + '\n')
                run.stdin.flush()
                client.send()
            except:
                break
    except:
        continue
