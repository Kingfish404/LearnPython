from django.db import models
import subprocess
from django.http import JsonResponse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# 主要功能函数
# Major function

def run_code(code):
    # 在服务器上运行代码
    div = code.split(sep="\n")
    # 如果输入的代码只是一行表达式，那就直接输出计算结果
    if(len(div)==1 and not 'print' in div[0] and not 'import' in div[0]):
        code = 'print('+code+')'
        print("edit:",code)
    try:
        output = subprocess.check_output(
            ['python', '-c', code], universal_newlines=True, stderr=subprocess.STDOUT,timeout=2)
    except Exception as e:
        output = e.output
    return output

@csrf_exempt
@require_POST
def api(request):
    # 解析代码的api
    code = request.POST.get('code')
    output = run_code(code)
    return JsonResponse({'output': output})

