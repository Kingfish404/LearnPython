# Python online

## 配置说明

>.
├── LearnPython            **Python实验界面**
│   ├── static
│   │   └── LearnPython    **css等文件**
│   └── templates
│       └── LearnPython    **Html文件**
├── siteProject
└── static              **全局静态文件**


## 环境要求

系统：Linux 或者 Window10

软件：Python3 以及 Django

### Debian/Ubuntu
```shell
# 配置环境
sudo apt install  python3
sudo apt install python3-pip
pip3 install django
```

### Redhat/CentOS
```shell
# 配置环境
sudo yum install  python3
sudo yum install python3-pip
pip3 install django
```

## 简介

利用django的配置，实现了一个简单的web服务器，返回浏览器提交的输入框中的python代码的运行结果并显示

## 运行方法
```shell
python3 online_app.py runserver
```
运行**start.sh**或**start.bat**

## REF

本项目参考过以下项目

https://github.com/Jet-ChenBo/online_python.git

感谢该作者[Jet-ChenBo](https://github.com/Jet-ChenBo)

2020-04-26