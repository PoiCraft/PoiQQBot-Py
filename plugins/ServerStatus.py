import psutil
import time
import config
from nonebot import on_command, CommandSession, permission

__plugin_name__ = '服务器状态'
__plugin_usage__ = r"""服务器状态
例：#status
或者 #服务器状态"""


@on_command('status', aliases='服务器状态', only_to_me=False, permission=permission.GROUP)
async def Bind(session: CommandSession):
    time.sleep(2)
    SenderQQNumber = session.ctx['user_id']
    SenderGroupNumber = session.ctx['group_id']
    if str(SenderGroupNumber) in config.SendGroup:
        pass
    else:
        CpuCoreInfoList = psutil.cpu_percent(1, True)
        CpuCoreInfo = ''
        i = 0
        while i < len(CpuCoreInfoList):
            CpuCoreInfo += f'核心{i + 1} -> {CpuCoreInfoList[i]}%\n'
            i += 1
        await session.send(f'[CQ:at,qq={SenderQQNumber}]\nCPU 总体占用率：{psutil.cpu_percent(True)}%\n内存总体使用率：{psutil.virtual_memory()[2]}%\n内存使用情况：{round(psutil.virtual_memory()[3]/1024/1024/1024, 2)}GB/{round(psutil.virtual_memory()[0]/1024/1024/1024, 2)}GB \nCPU核心占用率：\n{CpuCoreInfo}')