import pytest
import subprocess
import falcon
from falcon import testing
from Agent.ops.exe import run_cmd, run_script
from Agent.ops import deploy
from unittest.mock import MagicMock, patch
from Agent import app


@pytest.fixture
def client():
    return testing.TestClient(app.api)


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


def test_list_exe_script():
    script = [
        {
            'exe': ('mkdir -p ./test2', 'touch ./test2/2.txt', 'echo 1 > ./test2/2.txt', 'cat ./test2/2.txt'),
            'opt': True,
            'save_out': 'out',
            'cwd': '/tmp/'
        },
    ]

    ret = run_script(script)
    assert str(ret.get('out')).strip() == '1'


def test_get_local_hostname():
    run_ret = MagicMock()
    run_ret.stdout = 'hostname\n'
    with patch('subprocess.run', return_value=run_ret, autospec=True) as mock_func:
        hostname = deploy.get_local_hostname()
        assert 'hostname' in mock_func.call_args[0]
        mock_func.assert_called()
        assert hostname == 'hostname'


def test_api_get_hostname(client):
    run_ret = MagicMock()
    run_ret.stdout = 'hostname\n'
    with patch('subprocess.run', return_value=run_ret, autospec=True) as mock_func:
        resp = client.simulate_get('/hostname')
        mock_func.assert_called()
        assert resp.text == 'hostname'
        assert resp.status == falcon.HTTP_OK
