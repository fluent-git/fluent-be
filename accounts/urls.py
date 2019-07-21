from django.conf.urls import url
from django.urls import path
from rest_framework_nested import routers

from accounts import views


login_router = routers.SimpleRouter()
login_router.register('login', views.LoginViewSet, base_name='login')

logout_router = routers.SimpleRouter()
logout_router.register('logout', views.LogoutViewSet, base_name='logout')

profile_router = routers.SimpleRouter()
profile_router.register('profiles', views.ProfileViewSet, base_name='profiles')

queue_router = routers.SimpleRouter()
queue_router.register('queue', views.QueueViewSet, base_name='queue')

report_router = routers.SimpleRouter()
report_router.register('reports', views.ReportViewSet, base_name='reports')

review_router = routers.SimpleRouter()
review_router.register('reviews', views.ReviewViewSet, base_name='reviews')

user_router = routers.SimpleRouter()
user_router.register('users', views.UserViewSet, base_name='users')

talk_router = routers.SimpleRouter()
talk_router.register('talk', views.TalkViewSet, base_name='talk')


urlpatterns = [
    url(r'^analyze/$', views.Analyze.as_view(), name='analyze')
]

urlpatterns += queue_router.urls
urlpatterns += login_router.urls
urlpatterns += logout_router.urls
urlpatterns += profile_router.urls
urlpatterns += report_router.urls
urlpatterns += review_router.urls
urlpatterns += user_router.urls
urlpatterns += talk_router.urls
