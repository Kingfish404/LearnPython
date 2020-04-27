from django.db import models
import subprocess
from django.http import JsonResponse

# Create your models here.
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def run_code(code):
    # 在服务器上运行代码
    try:
        output = subprocess.check_output(
            ['python', '-c', code], universal_newlines=True, stderr=subprocess.STDOUT)
    except Exception as e:
        output = e.output
    return output


@csrf_exempt
@require_POST
def api(request):
    code = request.POST.get('code')
    output = run_code(code)
    return JsonResponse({'output': output})

