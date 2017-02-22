from django.conf.urls import url

from . import views

# 네임스페이스 지정.
app_name = 'polls'
urlpatterns = [
    # generic View 방식이 아닌 일반 방식 활용시는 아래와 같이.
    url(r'^$', views.index, name='index'),
    # detail 이라는 이름을 호출시 아래의 정규식에 일치하는 url로 이동
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),

    # specifics 라는 단어를 추가하려고 할 땐 아래와 같이 정의
    #url(r'^specifics/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),

    # generic view 활용시는 아래와 같이
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),

    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
