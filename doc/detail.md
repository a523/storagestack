### TODO:
- 支持debug模式启动？显示不同日志？


### HOWTO (实现细节)
#### 部署
##### 同步hosts
> 采用python-hosts第三方库
##### 管理节点到其他节点免密钥
>1. 通过http发送公钥到agent，agent填写密钥
>
>2. 通过`ssh-keygen -R 172.16.32.128`
删除对应的记录
>
>3. `ssh-keyscan -t ecdsa 172.16.32.128 >> known_hosts` 
获取目标主机公钥并添加到known_hosts

#### 用户管理
系统安装时默认创建一个超级用户：
```
user： admin
password： storage_stack
```
首次登录超级用户建议立即修改密码。
其他用户分管理员用户和普通用户(非敏感只读用户)和无任何权限用户。
通过web创建新用户，不可以是超级用户，可以是管理员。
超级用户只允许通过命令行创建。

只有超级用户才可以指配谁为管理员，管理员可以新建，删除，修改用户分组
普通用户通过加入不同组可以获得不同权限，或添加单项权限。
普通用户可以无任何权限，即只可以看出自己的个人中心。

以编程方式创建权限:
动态地创建用户权限， 通过post_migrate信号
https://docs.djangoproject.com/zh-hans/3.0/ref/signals/#django.db.models.signals.post_migrate

### DONE
- webServer, 中间件， 出现未捕获的错误，写日志，返回http
