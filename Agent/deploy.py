import os
from Agent.setting import BASE_DIR, config


# 部署前环境清理
def preflight_script():
    preflight = [
        {
            'exe': 'sudo yum install epel-release -y'
        },
        {
            'exe': 'sudo cp {} /etc/yum.repos.d/'.format(os.path.join(BASE_DIR, 'config/ceph.repo')),
            'is_ok': 'cat /etc/yum.repos.d/ceph.repo',
        },
        'yum makecache',
        {
            'exe': 'sudo yum install yum-plugin-priorities -y',
            'opt': True,
        },
        'sudo yum install ntp ntpdate ntp-doc -y',
        {
            'exe': 'sudo ntpdate pool.ntp.org',
            'try': 3,
        },
        'sudo systemctl restart ntpdate && systemctl restart ntpd && systemctl enable ntpd && systemctl enable ntpdate',
        'sudo systemctl stop firewalld',
        'sudo systemctl disable firewalld',

    ]
    return preflight

def update_all_hosts():
    pass