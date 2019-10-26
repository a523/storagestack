import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] [%(asctime)s] %(module)s.%(funcName)s: %(message)s',
            'datefmt': '%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'agent_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 日志文件定时删除
            'filename': '/var/log/storage_stack/agent.log',
            'when': 'D',
            'interval': 10,
            'backupCount': 2,
            'encoding': 'utf-8',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'agent': {
            'handlers': ['agent_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))