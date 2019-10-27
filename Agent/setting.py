import os
import pathlib
import yaml

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

BASE_DIR = pathlib.Path(__file__).parent
if os.path.exists('/etc/storage_stack/default.yaml'):
    config_file = '/etc/storage_stack/default.yaml'
else:
    config_file = BASE_DIR / 'config' / 'default.yaml'


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


config = get_config(config_file)