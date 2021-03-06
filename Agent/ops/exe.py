import subprocess
import time
from utils.decorator import general_log
import logging
import errors

logger = logging.getLogger('agent.exe')


@general_log('agent.exe')
def run_cmd(cmd, timeout=45, check=True, shell=True, **kwargs):
    """
    执行shell命令，在subprocess.run基础上封装一些默认参数和日志
    :param cmd:
    :param timeout:  超时时间
    :param check: 当执行出错的时候是否抛出异常
    :param shell:
    :return: 返回类subprocess.CompletedProcess
    """
    ret = subprocess.run(cmd, timeout=timeout, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check,
                         encoding='utf-8',
                         **kwargs)

    return ret


def run_script(script):
    result = {}
    for row in script:
        if isinstance(row, str):
            run_cmd(row)
        elif isinstance(row, dict):
            exe = row.get('exe')
            cwd = row.get('cwd')
            opt = row.get('opt', False)
            try_num = row.get('try', 1)  # default try once
            def_ok = row.get('def_ok')
            save_out = row.get('save_out')
            if (def_ok and not check_ok(def_ok)) or (not def_ok):
                for i in range(try_num):
                    try:
                        # 增加timeout参数并执行命令
                        if 'timeout' not in row.keys():
                            ret = run_exe(exe=exe, cwd=cwd, check=not opt)
                        else:
                            timeout = row['timeout']
                            ret = run_exe(exe=exe, timeout=timeout, cwd=cwd, check=not opt)
                        if opt and (not ret or ret.returncode != 0):
                            logger.warning('Execute command：“{}” failed, It\'s optional'.format(exe))
                            continue

                        # 是否捕获输出结果
                        if save_out:
                            if not (isinstance(save_out, str) or isinstance(save_out, int) or isinstance(save_out,
                                                                                                         tuple)):
                                raise errors.ScriptConfigError("Arg save_out mast be not variable")
                            if ret:
                                result[save_out] = ret.stdout
                    except subprocess.SubprocessError as e:
                        logger.warning('Execute command：“{}” failed, ready to retry: {}/{}'.format(exe, i + 1, try_num))
                        if i >= try_num - 1:
                            raise e
                    else:
                        break
                    time.sleep(i + 1 if i < 120 else 120)
            else:
                logger.debug('Ignore cmd {}, because check define status is ok'.format(exe))

        else:
            raise errors.ScriptConfigError('The row of script must be str or dict')
    return result


def run_exe(exe, *args, **kwargs):
    ret = None
    if isinstance(exe, str):
        ret = run_cmd(cmd=exe, *args, **kwargs)
    elif isinstance(exe, list) or isinstance(exe, tuple):
        check = kwargs.get('check')
        if not exe:
            raise errors.ScriptConfigError('Arg exe is None')
        for i, cmd in enumerate(exe):
            r = run_cmd(cmd=cmd, *args, **kwargs)

            if (check is False) and (r.returncode != 0):  # 当整体为可选的时候，任何一个有失败， 后面的不执行
                break

            if i == len(exe) - 1:
                ret = r  # only save last return

    else:
        raise errors.ScriptConfigError('Arg exe must be str or iterable object')
    return ret


def check_ok(def_ok):
    """
    检查状态是否达到ok，
    shell 输出0，算成功， 1， 失败
    python 函数，返回True 算ok，
    :param def_ok: 判断状态的命令
    :return:
    """
    if isinstance(def_ok, str):
        ret = run_cmd(def_ok)
        if str(ret.stdout).strip() == '0':
            return True
        else:
            return False
    elif callable(def_ok):
        return def_ok()
    else:
        raise errors.ScriptConfigError("The def_ok option mast be str for shell or a callable object for python")
