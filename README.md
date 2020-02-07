# storagestack
>让ceph更容易使用

### 小目标：
- 即可以一键安装部署全新的ceph

- 也可以管理监控已经存在的ceph

- 通过命令操作的ceph配置在平台同样可见

- 易于理解和二次开发

### 架构
- Control Server
- Agent
- Web UI


### TODO LIST
1. 安装集群
    - 基本web 后端 和 agent
2. 用户登录和权限
    
### QuickStart
#### AGENT
> AGENT 需要部署在集群中的每个节点上
##### 开发环境部署：
- 启动agent服务
```shell
gunicorn --reload  Agent.app:api --bind 0.0.0.0:8600
```

#### WebServer
在Linux或Unix系统上请先创建文件夹 /var/log/storage_stack,
并赋予权限
```shell
python manage.py runserver
```
