import os
import re
import sys
import time
import config
import asyncio
import threading
import subprocess
import websockets

SendInfo = 'None'  # 线程里面的东西返回值
ServerRun = subprocess.Popen(config.BEDROCKSERVEREXE,
                             shell=False,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             universal_newlines=True)


# 让用户以为这真的是一个控制台(Doge)
def OutputInfo():
    while True:
        time.sleep(0.2)
        Info = ServerRun.stdout.readline().strip()
        global SendInfo
        SendInfo = Info  # 传出去
        if Info == '':
            print('服务器异常结束，即将重启')
            RestartServer()
        elif Info == 'Quit correctly':
            print('已经结束运行了，关掉窗口即可')
            raise SystemExit
        elif Info is not None and Info != 'Unknown command: . Please check that the command exists and that you have permission to use it.':
            print('--->', Info)


# 用户输入，不然控制台是模拟不完整的！
def ListenConsoleCommand():
    while True:
        command = input("> ")
        ServerRun.stdin.write('{0}\n'.format(command))
        ServerRun.stdin.flush()


threading.Thread(target=ListenConsoleCommand).start()
threading.Thread(target=OutputInfo).start()


# 重启服务器
def RestartServer():
    python = sys.executable
    os.execl(python, python, *sys.argv)


# ws部分
async def ExecCommand(websocket: object, path: object) -> object:
    while True:
        Command = await websocket.recv()
        print('服务器收到并执行---> ', Command)
        time.sleep(0.1)
        ServerRun.stdin.write(Command + '\n')
        ServerRun.stdin.flush()
        time.sleep(0.1)
        if SendInfo == 'Unknown command: . Please check that the command exists and that you have permission to use it.':
            print('Success')
            await websocket.send('Success')
        elif re.search('^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} INFO].+', SendInfo):
            print('Success')
            await websocket.send('Success')
        else:
            await websocket.send(SendInfo)
        ServerRun.stdin.write('' + '\n')
        ServerRun.stdin.flush()


StartWsServer = websockets.serve(ExecCommand, '127.0.0.1', 30000)
asyncio.get_event_loop().run_until_complete(StartWsServer)
asyncio.get_event_loop().run_forever()
time.sleep(6)
ServerRun.stdin.write('' + '\n')
ServerRun.stdin.flush()