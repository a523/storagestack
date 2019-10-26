import os
from Agent.setting import BASE_DIR

# 部署前环境清理
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
        'exe': 'sudo yum install openssh-server -y',
        'opt': True,
    },
    'sudo yum install ntp ntpdate ntp-doc -y',
    {
        'exe': 'sudo ntpdate pool.ntp.org',
        'try': 3,
    },
    'sudo systemctl restart ntpdate && systemctl restart ntpd && systemctl enable ntpd && systemctl enable ntpdate',
]


