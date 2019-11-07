"""功能测试，测试前请先启动服务"""

import requests


def test_server_status():
    resp = requests.get('http://localhost:8600/hello')
    assert resp.status_code == 200, 'Agent web server unavailable'
    assert resp.text == 'Hello, World'
