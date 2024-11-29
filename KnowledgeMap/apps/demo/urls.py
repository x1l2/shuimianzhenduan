from django.urls import path, re_path
from demo import views, tests

urlpatterns = [
    path('', tests.index),
    path('index/', tests.test),
    re_path('index/test/', tests.test),
    path('index/test1/',tests.test1),
]