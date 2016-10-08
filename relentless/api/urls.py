from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import Login, Logout, UserList, UserDetail


urlpatterns = [
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', Logout.as_view()),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
