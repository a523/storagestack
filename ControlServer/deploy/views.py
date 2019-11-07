from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests


# def gen_node_agent_url(ip):

@api_view(['GET'])
def check_conn(request):
    """检查node上的Agent是否可以连通"""
    ip = request.GET['ip']
    resp = requests.get("http://{}:{}/hello".format(ip, 8600))
    if resp.ok:
        return Response('ok')
