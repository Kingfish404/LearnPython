from django.test import SimpleTestCase
from django.test import TestCase
from .models import run_code
from .models import timeOut

# Create your tests here.
# 导入设置文件

import sys
import os
sys.path.append(os.getcwd())
from config import *

class models_api_Test(TestCase):

    def test_self(self):
        code = '2**10'
        result = '1024'
        self.assertEqual(run_code(code).output, result)

    def test_cmd(self):
        self.assertEqual(run_code('1+1').output, '2')

    def test_print(self):
        self.assertEqual(run_code('print(2**10)').output, '1024')

    def test_timeout(self):
        code = "from timeit import repeat\ndef func():\n\
            s = 0\nfor i in range(10000):\n\
            t = repeat('func()', 'from __main__ import func', number=100, repeat=500)\n"
        self.assertEqual(
            run_code(code).output, '计算超时,'+timeOutMsg+'\n运行时间不得超过 '+str(timeOut)+' 秒')
