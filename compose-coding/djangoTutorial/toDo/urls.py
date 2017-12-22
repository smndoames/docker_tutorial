from django.conf.urls import url

from . import views

app_name = 'toDo'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^clear/$',
        views.ClearSelectedView.as_view(), name='clear_selected'),
    url(r'^(?P<pk>[0-9]+)/curated/$',
        views.CurateTodo.as_view(), name='curated_todo'),
]
