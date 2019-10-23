import pytest
from Agent.exe import run_cmd

import subprocess


def test_run_cmd_success():
    ret = run_cmd('python3 --version')
    assert ret.returncode == 0
    assert 'Python 3' in ret.stdout


def test_run_cmd_error():
    with pytest.raises(subprocess.CalledProcessError) as e:
        run_cmd('notexitcmd')
    assert ('未找到命令' in e.value.stderr) or ('not exit' in e.value.stderr)
