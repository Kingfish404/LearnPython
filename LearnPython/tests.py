from django.test import SimpleTestCase
from django.test import TestCase
from .models import run_code
from .models import timeOut
# Create your tests here.


class models_api_Test(TestCase):

    def test_self(self):
        code = '2**10'
        result = '1024'
        self.assertEqual(run_code(code), result)

    def test_cmd(self):
        self.assertEqual(run_code('1+1'), '2')

    def test_print(self):
        self.assertEqual(run_code('print(2**10)'), '1024')

    def test_empty(self):
        self.assertEqual(run_code('  '), '请输入代码')

    def test_timeout(self):
        code = "from timeit import repeat\ndef func():\n\
            s = 0\nfor i in range(10000):\n\
            t = repeat('func()', 'from __main__ import func', number=100, repeat=500)\n"
        self.assertEqual(
            run_code(code), '计算超时,请简化你的代码\n运行时间不得超过 '+str(timeOut)+' 秒')
