import multiprocessing

bind = '0.0.0.0:8600'
proc_name = 'agent'

workers = multiprocessing.cpu_count() * 2 + 1
threads = 4
backlog = 2048  # 服务器中在pending状态的最大连接数，即client处于waiting的数目。超过这个数目， client连接会得到一个error。
worker_connections = 1000
daemon = True
debug = False
worker_class = 'gevent'
accesslog = '/var/log/agent/gunicorn-access.log'
errorlog = '/var/log/agent/gunicorn-error.log'
