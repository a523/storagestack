import subprocess
import logging

logger = logging.getLogger('control_server.exe')


def run_cmd(cmd, timeout=45, check=True, shell=True, **kwargs):
    """
    执行shell命令，在subprocess.run基础上封装一些默认参数和日志
    :param cmd:
    :param timeout:  超时时间
    :param check: 当执行出错的时候是否抛出异常
    :param shell:
    :return: 返回类subprocess.CompletedProcess
    """
    logger.debug('Starting run cmd {}, timeout: {}'.format(cmd, timeout))
    try:
        ret = subprocess.run(cmd, timeout=timeout, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             check=check,
                             encoding='utf-8',
                             **kwargs)
        logger.debug('return: {}: {}'.format(ret.returncode, ret.stdout))
        return ret
    except subprocess.CalledProcessError as e:
        logger.exception("{0} Why: {1}".format(e, e.stderr))
        raise e
    except Exception as e:
        logger.exception(e)
        raise e
