from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

# Create your views here.
# 界面控制
from django.http import HttpResponse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'LearnPython/index.html'

    def get_queryset(self):
        pass
