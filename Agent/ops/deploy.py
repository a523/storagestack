import os
from Agent.setting import BASE_DIR, config


# 部署前环境清理
def preflight_script():
    preflight = [
        {
            'exe': 'sudo yum install epel-release -y',
            'timeout': 60 * 4,
        },
        {
            'exe': 'sudo cp {} /etc/yum.repos.d/'.format(os.path.join(BASE_DIR, 'config/ceph.repo')),
            'is_ok': 'cat /etc/yum.repos.d/ceph.repo',
        },
        {
            'exe': 'yum makecache',
            'opt': True,
            'try': 2,
            'timeout': 60 * 15
        },
        {
            'exe': 'sudo yum install yum-plugin-priorities -y',
            'opt': True,
            'timeout': 60 * 8
        },
        'sudo yum install ntp ntpdate ntp-doc -y',
        {
            'exe': 'sudo ntpdate pool.ntp.org',
            'try': 3,
            'timeout': 60,
            'def_ok': 'if [ `ps aux | grep ntpd | wc -l` -gt 1 ]; then echo 0; else echo 1; fi'
        },
        'sudo systemctl stop ntpd; sudo systemctl restart ntpdate',
        'sudo systemctl restart ntpd',
        'sudo systemctl enable ntpd; sudo systemctl enable ntpdate',
        'sudo systemctl stop firewalld',
        'sudo systemctl disable firewalld',
    ]
    return preflight


def update_all_hosts():
    pass
