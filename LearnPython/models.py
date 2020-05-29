from config import *
from django.db import models
import subprocess
from subprocess import TimeoutExpired
from django.http import JsonResponse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import time
import re

import hashlib
import json
import requests

# 导入设置文件
import sys
import os
sys.path.append(os.getcwd())

# 主要功能函数
# Major function


class Data:
    # 运行代码的数据文件
    code = str()
    output = str()
    time = float()
    safe = bool()


class Post():
    # 网页数据的储存文件
    title = ""
    body = ""
    __PostPath = os.getcwd()+POST

    def __str__(self):
        pass

    def readPost(self, postName="0"):
        try:
            path = self.__PostPath+str(postName)+'.md'
            f = open(path, 'r', encoding='utf-8', newline='\n')
        except FileNotFoundError as e:
            self.body = Msg404
            self.reformat2markdown()
        except Exception as e:
            self.body = "Error"
        else:
            self.body = f.read()
            f.close()


class TestData():
    # 题目的读取文件
    Type = 0       # 题目类型，0为选择，1为判断
    num = 0         # 当前第几题
    TestData = ""

    __TestPath = os.getcwd()+POST

    def read(self):
        try:
            path = self.__TestPath+TestName
            f = open(path, 'r', encoding='utf-8', newline='\n')
            jsonData = f.read()

            Data = json.loads(jsonData, encoding="utf-8")
            print(self.Type)
            if(self.Type == 0):
                if(self.num < len(Data['choice'])):
                    self.TestData = Data['choice'][self.num]
                else:
                    self.quest = "Num ERROR"
                    self.TestData = Data['error'][0]
                    return
            elif(self.Type == 1):
                if(self.num < len(Data['charge'])):
                    self.TestData = Data['charge'][self.num]
                else:
                    self.quest = "Num ERROR"
                    self.TestData = Data['error'][0]
                    return
        except FileNotFoundError:
            self.quest = "Error,file not found"
            
            


def safeChack(data):
    # 对代码进行安全检测
    disableShell = ['ps', 'cat', 'rm', 'cd', 'vi', 'vim',
                    'ls', 'dir', 'mv', 'cmd', 'reboot']
    # 对不安全命令进行警告替换
    for shell in disableShell:
        _str = re.subn(r'system(.*[\"\'].*'+shell+'.*[\"\'].*)',
                       "system(\"echo 为了系统安全,shell的 "+shell+" 命令是不允许使用的\")", data.code, 0, re.IGNORECASE)
        data.code = _str[0]
    data.safe = True


def errorTranslate(errorData):
    # 错误类型
    errorTypeReg = [[r'SystemExit:', "解释器请求退出:"],
                    [r'OverflowError:', "数值运算超出最大限制:"],
                    [r'IOError:', "	输入/输出操作失败:"],
                    [r'NameError:', "名称错误:"],
                    [r'IndexError:', "索引错误:"],
                    [r'SyntaxError:', "语法错误:"],
                    [r'Unbound LocalError:', "未绑定的本地错误:"],
                    [r'IndentationError:', "缩进错误:"],
                    [r'NotImplementedError:', "尚未实现的方法:"],
                    [r'ZeroDivisionError:', "除零错误:"],
                    [r'AttributeError:', "对象没有这个属性:"],
                    [r'ImportError:', "导入失败:"],
                    [r'ModuleNotFoundError:', "模块错误:"]
                    ]

    # 错误语句
    errorReg = [[r'Traceback \(most recent call last\):', "异常跟踪 (最近一次错误信息):"],
                [r'line ([1-9]*)', " 第\\1行 "],
                [r' File', "代码"],
                [r'in <(.*)>', "位于 <\\1>"],
                [r' name (.*) is not defined', "  \\1  未被定义或者声明"],
                [r'No module named (\'.*\')', "没有 \\1 这个模块"],
                [r'list index out of range', "列表索引超出范围"],
                [r'invalid syntax', "无效的语法"],
                [r'Did you mean ([^?]*)?', "你是想使用 \\1 吗"],
                [r'Unbound LocalError:', "未绑定的本地错误:"],
                [r'division by zero', "除以零"],
                [r'Missing parentheses in call to (\'print\')',
                 "调用 \\1 时缺少括号"],
                ]
    for i in range(len(errorTypeReg)):
        errorData = re.sub(errorTypeReg[i][0], errorTypeReg[i][1], errorData)
    for i in range(len(errorReg)):
        errorData = re.sub(errorReg[i][0], errorReg[i][1], errorData)
    return errorData


def run_code(code):
    data = Data()
    output = str()
    errors = str()
    pythonV = "python"
    # 在服务器上运行代码
    div = code.split(sep="\n")
    # 如果输入的代码只是一行表达式，那就直接输出计算结果
    if(len(div) == 1 and not 'print' in div[0] and not 'import' in div[0]):
        data.code = 'print('+code+')'
    else:
        data.code = code

    safeChack(data)
    if 'linux' in sys.platform:
        pythonV = "python3"

    timeStart = time.time()
    # 建立Python子进程
    subp = subprocess.Popen(
        [pythonV, '-c', data.code], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        output, errors = subp.communicate(timeout=timeOut)
        data.time = time.time()-timeStart
    except TimeoutExpired:
        output = '计算超时,'+timeOutMsg+'\n运行时间不得超过 '+str(timeOut)+' 秒'
        data.time = "3"
    except Exception as e:
        output = "内部出现错误"
    finally:
        # 结束子进程
        subp.kill()
        if(errors != ""):
            output = errorTranslate(errors)
    if(len(output) > 0 and output[-1] == '\n'):
        output = output[:-1]

    data.output = output
    return data


def translate(output):
    # register re
    re_output = r'([a-zA-Z]*?Error|Warning.*):(.*)'
    #rp_output =r'[a-zA-Z]*?Error|Warning:.*'
    tr_output = re.compile(re_output, re.S).findall(output)
    new_tr_output = tr_output[0][0] + ':' + tr_output[0][1]
    # 有道词典 api
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    # 传输的参数，其中 i 为需要翻译的内容
    appid = "20200521000464395"
    salt = "1435660288"
    key = "IjQ_kAmRPlox3ROV0eL4"
    q = output
    sign_str = appid + q + salt + key
    encode_sign = sign_str.encode(encoding='utf-8')
    md5 = hashlib.md5()
    md5.update(encode_sign)
    sign_md5 = str(md5.hexdigest())
    key = {
        'q': q,
        'from': 'en',
        "to": "zh",
        "appid": appid,
        "salt": salt,
        "sign": sign_md5,
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key, headers={
                             'Content-Type': 'application/x-www-form-urlencoded'}).text

    f_output_dict = json.loads(response)
    results = f_output_dict['trans_result']
    f_output = ''
    for result in results:
        f_output = f_output + result['dst'] + '\n'
    #f_output = f_output_dict['trans_result']
    # print(f_output_dict)

    # return re.sub(rp_output,f_output,output)
    return f_output


@csrf_exempt
@require_POST
def api(request):
    # 解析代码的api
    code = request.POST.get('code')
    data = run_code(code)
    return JsonResponse({'output': data.output, 'time': data.time})


@csrf_exempt
@require_POST
def getTest(request):
    # 获取题目的api
    
    data = TestData()
    data.Type = int(request.POST.get('Type'))
    data.num = int(request.POST.get('num'))
    data.read()
    return JsonResponse(data.TestData)
    
