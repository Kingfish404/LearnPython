import subprocess
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

setting = {
    'DEBUG': True,
    'ROOT_URLCONF': __name__
}

settings.configure(**setting)


def home(request):
    with open('./index.html', 'rb') as f:
        html = f.read()
    return HttpResponse(html)


@csrf_exempt
@require_POST
def api(request):
    code = request.POST.get('code')
    output = run_code(code)
    return JsonResponse({'output': output})


def run_code(code):
    # 在服务器上运行代码
    try:
        output = subprocess.check_output(
            ['python3', '-c', code], universal_newlines=True, stderr=subprocess.STDOUT)
    except Exception as e:
        output = e.output
    return output


urlpatterns = [
    url(r'^api/$', api),
    url(r'^', home),
]

if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
