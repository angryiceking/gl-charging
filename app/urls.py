from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import IndexView, CodeView


app_name = 'app'
urlpatterns = [
    path('', csrf_exempt(IndexView.as_view()), name='index'),
    path('code/', csrf_exempt(CodeView.as_view()), name='code'),
]

