from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

# Create your views here.
# 界面控制
from django.http import HttpResponse
from django.views import generic
from .models import Post


class IndexView(generic.ListView):
    template_name = 'LearnPython/index.html'

    def get_queryset(self):
        pass

class RoadView(generic.ListView):
    template_name = 'LearnPython/road.html'

    def get_queryset(self):
        pass

class LoadingView(generic.ListView):
    template_name = 'LearnPython/loading.html'

    def get_queryset(self):
        pass


def doc(request, pk=0):
    # 渲染markdown读取并返回
    post = Post()
    post.title = pk
    post.readPost(pk)
    return render(request, 'LearnPython/doc.html', context={'post': post})

def Default(request,pk="404"):
    post = Post()
    post.title = pk
    post.readPost(pk)
    return render(request, 'LearnPython/doc.html', context={'post': post})
