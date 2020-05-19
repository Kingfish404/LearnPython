from django.urls import path
from django.conf.urls import url

from . import views
from . import models

# url设置

app_name = 'LearnPython'
urlpatterns = [
    url(r'^api/$', models.api),
    path('', views.IndexView.as_view()),
    path('road/', views.RoadView.as_view()),
    path('doc/', views.doc, name='doc'),
    path('doc/<str:pk>', views.doc, name='doc'),
    path('loading/', views.LoadingView.as_view()),
]