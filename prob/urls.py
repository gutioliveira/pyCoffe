from django.conf.urls import url

from . import views

app_name = 'prob'
urlpatterns = [
    url(r'detail/', views.detail, name='detail'),
    url(r'local_image/', views.localImage, name='localImage'),
    url(r'^$', views.index, name='index'),
]
