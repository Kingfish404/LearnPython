# HelloPython

## 配置说明

>.  
├── LearnPython         **Python实验界面**  
│   ├── static          **css等文件**  
│   │   └── LearnPython
│   └── templates       **Html文件**  
│       └── LearnPython
├── post                **文档文件**
├── siteProject         **项目设置**
└── static              **全局静态文件**  


## 环境要求

系统：Linux 或者 Window10

软件：Python3.6+ 以及Python包：Django,requests与 Sqlite3(可以无)

### Debian/Ubuntu
```shell
# 配置Deb系列服务器环境
sudo apt install  python3
sudo apt install python3-pip
pip3 install django
pip3 install requests
```

### Redhat/CentOS
```shell
# 配置服务器环境
sudo yum install  python3
sudo yum install python3-pip
pip3 install django
pip3 install requests
```

## 简介

利用django的配置，实现了一个简单的web服务器，返回浏览器提交的输入框中的python代码的运行结果并显示

## 运行方法
```shell
python3 manage.py runserver
# 或者
python manage.py runserver
```
Windows平台可以运行**start.bat**

## 测试方法
```shell
python manage.py test
# 或者
python3 manage.py test
```

## 注意

暂无

## REF

本项目参考过以下项目

https://github.com/Jet-ChenBo/online_python.gite

感谢该作者[Jet-ChenBo](https://github.com/Jet-ChenBo)

2020-05-28