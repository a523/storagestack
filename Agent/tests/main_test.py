import pytest
import subprocess
from Agent.exe import run_cmd, run_script
from Agent.setting import config


def test_run_cmd_success():
    ret = run_cmd('python3 --version')
    assert ret.returncode == 0
    assert 'Python 3' in ret.stdout


def test_run_cmd_error():
    with pytest.raises(subprocess.CalledProcessError) as e:
        run_cmd('notexitcmd')
    assert ('未找到命令' in e.value.stderr) or ('not exit' in e.value.stderr)


def test_run_script():
    test_opt_and_cwd = [
        {
            'exe': 'touch 2.txt',
            'cwd': '/tmp/test',
            'def_ok': 'if [-f /tmp/test/2.txt];then echo 0 ; else echo 1;fi',
        },
        {
            'exe': 'exit 1',
            'cwd': '/tmp/test',
            'opt': True
        }
    ]

    script = [
        "ls",
        "mkdir -p /tmp/test/",
        {
            'exe': "cd /tmp/test && echo hello > 1.txt",
            'def_ok': "if [ -s /tmp/test/1.txt ];then echo 0;else echo 1;fi"
        },
        {
            'exe': 'cat /tmp/test/1.txt',
            'save_out': 'result',
        },
        *test_opt_and_cwd,
    ]
    ret = run_script(script)
    assert ret['result'] == "hello\n"


def test_yaml_config():
    assert config.get('username') == 'easy_ceph'
