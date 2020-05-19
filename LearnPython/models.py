from django.db import models
import subprocess
from django.http import JsonResponse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import markdown
import time
import sys
import os
import re

# 主要功能函数
# Major function

timeOut = 3


class Data:
    code = str()
    output = str()
    time = float()
    safe = bool()

# 对代码进行安全检测


def safeChack(data):
    disableShell = ['ps', 'cat', 'rm', 'cd',
                    'ls', 'dir', 'mv', 'cmd', 'reboot']
    # 对不安全命令进行警告替换
    for shell in disableShell:
        _str = re.subn(r'system(.*[\"\'].*'+shell+'.*[\"\'].*)',
                       "system(\"echo 为了系统安全,shell的 "+shell+" 命令是不允许使用的\"))", data.code, 0, re.IGNORECASE)
        data.code = _str[0]
    data.safe = True


def run_code(code):
    data = Data()
    # 在服务器上运行代码
    div = code.split(sep="\n")
    # 如果输入的代码只是一行表达式，那就直接输出计算结果
    if(len(div) == 1 and not 'print' in div[0] and not 'import' in div[0]):
        code = 'print('+code+')'
    try:
        data.code = code
        safeChack(data)
        if(data.safe):
            timeStart = time.time()
            if 'linux' in sys.platform:
                output = subprocess.check_output(
                    ['python3', '-c', data.code], universal_newlines=True, stderr=subprocess.STDOUT, timeout=timeOut)
            else:
                output = subprocess.check_output(
                    ['python', '-c', data.code], universal_newlines=True, stderr=subprocess.STDOUT, timeout=timeOut)
            data.time = time.time()-timeStart
    except subprocess.TimeoutExpired as e:
        output = '计算超时,请简化你的代码\n运行时间不得超过 '+str(e.timeout)+' 秒'
        data.time = "3"
    except Exception as e:
        output = e.output
        translate(output)
    if(output[-1] == '\n'):
        output = output[:-1]
    if(output == ''):
        output = '请输入代码'
        data.time = 0
    data.output = output
    return data


@csrf_exempt
@require_POST
def api(request):
    # 解析代码的api
    code = request.POST.get('code')
    data = run_code(code)
    return JsonResponse({'output': data.output, 'time': data.time})


class Post():
    title = ""
    body = ""
    __PostPath = os.getcwd()+"/post/"

    def __str__(self):
        pass

    def readPost(self, postName="0"):
        try:
            path = self.__PostPath+str(postName)+'.md'
            f = open(path, 'r', encoding='utf-8', newline='\n')
        except FileNotFoundError as e:
            str404 = "好像到了奇怪的地方"
            self.body = '# 404, '+str(postName)+' file not found\n'+str404
            self.reformat2markdown()
        except Exception as e:
            self.body = "Error"
        else:
            self.body = f.read()
            f.close()

    def reformat2markdown(self):
        self.body = markdown.markdown(self.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
