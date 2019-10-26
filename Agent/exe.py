import subprocess
from Agent.util.decorator import general_log
import logging
from Agent import errors

logger = logging.getLogger('agent.exe')


@general_log('agent.exe')
def run_cmd(cmd, timeout=30, check=True, shell=True, **kwargs):
    """
    执行shell命令，在subprocess.run基础上封装一些默认参数和日志
    :param cmd:
    :param timeout:  超时时间
    :param check: 当执行出错的时候是否抛出异常
    :param shell:
    :return: 返回类subprocess.CompletedProcess
    """
    ret = subprocess.run(cmd, timeout=timeout, shell=shell, capture_output=True, check=check, encoding='utf-8',
                         **kwargs)

    return ret


def run_script(script):
    result = {}
    for row in script:
        if isinstance(row, str):
            run_cmd(row)
        elif isinstance(row, dict):
            exe = row.get('exe')
            opt = row.get('opt', False)
            try_num = row.get('try', 1)  # default try once
            def_ok = row.get('def_ok')
            save_out = row.get('save_out')
            if (def_ok and not check_ok(def_ok)) or (not def_ok):
                for i in range(try_num):
                    try:
                        if 'timeout' not in row.keys():
                            ret = run_cmd(cmd=exe, check=not opt)
                        else:
                            timeout = row['timeout']
                            ret = run_cmd(cmd=exe, timeout=timeout, check=not opt)

                        if save_out:
                            if not (isinstance(save_out, str) or isinstance(save_out, int) or isinstance(save_out,
                                                                                                         tuple)):
                                raise errors.ScriptConfigError("Arg save_out mast be not variable")
                            result[save_out] = ret.stdout
                            return result
                    except Exception as e:
                        if i >= try_num - 1:
                            raise e
            else:
                logger.debug('Ignore cmd {}, because check define status is ok'.format(exe))

        elif isinstance(row, list) or isinstance(row, tuple):
            return run_script(row)


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
        if str(ret.stdout) == '0':
            return True
        else:
            return False
    elif callable(def_ok):
        return def_ok()
    else:
        raise errors.ScriptConfigError("The def_ok option mast be str for shell or a callable object for python")
