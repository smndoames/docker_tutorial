from django.conf.urls import url

from . import views

app_name = 'toDo'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
