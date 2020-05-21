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

import hashlib
import json
import requests

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


def errorTranslate(errorData):
    # 错误类型
    errorTypeReg = [[r'SystemExit:', "解释器请求退出:"],
                    [r'OverflowError:', "数值运算超出最大限制:"],
                    [r'IOError:', "	输入/输出操作失败:"],
                    [r'NameError:', "变量名错误:"],
                    [r'IndexError:', "索引错误:"],
                    [r'SyntaxError:', "语法错误:"],
                    [r'Unbound LocalError:', "未绑定的本地错误:"],
                    [r'IndentationError:', "缩进错误:"],
                    [r'NotImplementedError:', "尚未实现的方法:"]
                    ]
    
    # 错误语句
    errorReg = [[r'Traceback \(most recent call last\):', "异常跟踪 (最近一次错误信息):"],
                [r'line ([1-9]*)', " 第\\1行 "],
                [r' File', "代码"],
                [r'in <(.*)>', "位于 <\\1>"],
                [r' name (.*) is not defined', "  \\1  未被定义或者声明"],
                [r'list index out of range', "列表索引超出范围"],
                [r'invalid syntax', "无效的语法"],
                [r'Did you mean ([^?]*)?', "你是想使用 \\1 吗"],
                [r'Unbound LocalError:', "未绑定的本地错误:"],
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
        output = translate(e.output)
    if(output[-1] == '\n'):
        output = output[:-1]
    if(output == ''):
        output = '请输入代码'
        data.time = 0
    data.output = output
    return data

def translate(output):
    #register re
    re_output = r'([a-zA-Z]*?Error|Warning.*):(.*)'
    #rp_output =r'[a-zA-Z]*?Error|Warning:.*'
    tr_output = re.compile(re_output,re.S).findall(output)
    new_tr_output = tr_output[0][0] + ':' +tr_output[0][1]
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
    response = requests.post(url, data=key,headers={'Content-Type':'application/x-www-form-urlencoded'}).text
    
    f_output_dict = json.loads(response)
    results = f_output_dict['trans_result']
    f_output = ''
    for result in results:
        f_output = f_output  + result['dst'] + '\n'
    #f_output = f_output_dict['trans_result']
    #print(f_output_dict)
        
    #return re.sub(rp_output,f_output,output)
    return f_output
    
    
    
    

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
