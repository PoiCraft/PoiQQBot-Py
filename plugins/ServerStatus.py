import psutil
import time
from nonebot import on_command, CommandSession

__plugin_name__ = '服务器状态'
__plugin_usage__ = r"""服务器状态
例：#status
或者 #服务器状态"""


@on_command('status', aliases='服务器状态', only_to_me=False)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']
    CpuCoreInfoList = psutil.cpu_percent(1, True)
    await session.send(f'[CQ:at,qq={SenderQQNumber}]请稍后，正在计算中...')
    CpuCoreInfo = ''
    i = 0
    while i < len(CpuCoreInfoList):
        CpuCoreInfo += f'核心{i + 1} -> {CpuCoreInfoList[i]}%  '
        i += 1
    await session.send('[CQ:at,qq=%s] CPU总体占用率：%s%s\nCPU核心占用率：%s\n内存总体使用率：%.2f %s  使用情况:%.2fGB/%.2fGB' % (
        SenderQQNumber, psutil.cpu_percent(True), '%', CpuCoreInfo, float(psutil.virtual_memory()[2]), '%',
        float(psutil.virtual_memory()[1] / 1024 / 1024 / 1024), float(psutil.virtual_memory()[0] / 1024 / 1024 / 1024)))
