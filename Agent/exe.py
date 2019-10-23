import subprocess
from Agent.util.decorator import general_log


@general_log('agent.exe')
def run_cmd(cmd: str, timeout=30, check=True, **kwargs):
    """
    执行shell命令，在subprocess.run基础上封装一些默认参数和日志
    :param cmd:
    :param timeout:  超时时间
    :param check: 当执行出错的时候是否抛出异常
    :return: 返回类subprocess.CompletedProcess
    """
    ret = subprocess.run(cmd, timeout=timeout, shell=True, capture_output=True, check=check, encoding='utf-8',
                         **kwargs)

    return ret
