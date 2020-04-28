from django.test import SimpleTestCase
from django.test import TestCase
from .models import run_code
from .models import timeOut
# Create your tests here.

class modelsTest(TestCase):
    def test_self(self):
        code='1+1'
        result='2'
        self.assertEqual(run_code(code), result)

    def test_cmd(self):
        self.assertEqual(run_code('1+1'), '2')

    def test_print(self):
        self.assertEqual(run_code('print(2**10)'), '1024')

    def test_empty(self):
        self.assertEqual(run_code('  '), '请输入代码')



    # def test_timeout(self):
    #     code="from timeit import repeat\ndef func():\n\
    #         s = 0\nfor i in range(10000):\n\
    #         t = repeat('func()', 'from __main__ import func', number=100, repeat=500)\n"
    #     self.assertEqual(run_code(code), '计算超时,请简化你的代码\n运行时间不得超过 '+str(timeOut)+' 秒')

# from timeit import repeat

# def func():
#     s = 0
#     for i in range(1000):
#         s += i
# #repeat和timeit用法相似，多了一个repeat参数，表示重复测试的次数(可以不写，默认值为3.)，返回值为一个时间的列表。
# t = repeat('func()', 'from __main__ import func', number=100, repeat=500)
# print(t) 
# print(min(t))