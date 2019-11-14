import requests
from django.conf import settings


def gen_node_agent_url(ip, path):
    try:
        scheme = settings.AGENT_SCHEME
        port = settings.AGENT_PORT
    except AttributeError as e:
        scheme = 'http'
        port = '8600'
    url = "{protocol}://{ip}:{port}/{path}".format(protocol=scheme, ip=ip, port=port, path=path)
    return url


def is_ok(code):
    """http status is ok"""
    if 300 > int(code) >= 200:
        return True
    else:
        return False
# def request_agent(ip, path, method, args=None):
#     pass
