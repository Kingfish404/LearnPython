# Python online

## 配置说明

>.  
├── LearnPython            **Python实验界面**  
│   ├── static      **css等文件**  
│   │   └── LearnPython
│   └── templates      **Html文件**  
│       └── LearnPython
├── siteProject  **项目设置**
└── static              **全局静态文件**  


## 环境要求

系统：Linux 或者 Window10

软件：Python3.6+ 以及 Django 与 Sqlite3

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
python3 manage.py runserver
# 或者
python manage.py runserver
```
运行**start.sh**或**start.bat**

## 测试方法
```shell
python manage.py test
# 或者
python3 manage.py test
```

## 注意

默认的代码执行命令为python,如果在Linux平台运行，且希望执行pyhton3版本
推荐用以下命令
```shell
sudo mv /usr/bin/python /usr/bin/python_backup
sudo ln -s /usr/bin/python3 /usr/bin/python
```

将python命令指向python3

## REF

本项目参考过以下项目

https://github.com/Jet-ChenBo/online_python.git

感谢该作者[Jet-ChenBo](https://github.com/Jet-ChenBo)

2020-04-26