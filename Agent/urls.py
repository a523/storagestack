from Agent import views

paths = [
    ('/hello', views.HelloViews()),
    ('/hostname', views.HostName()),
    ('/hosts', views.Hosts()),
    ('/ssh-key', views.SshKey()),
]