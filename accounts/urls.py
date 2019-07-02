from django.conf.urls import url
from django.urls import path
from rest_framework_nested import routers

from accounts import views


find_chat_router = routers.SimpleRouter()
find_chat_router.register('find-chat', views.FindChatViewSet, base_name='find-chat')

login_router = routers.SimpleRouter()
login_router.register('login', views.LoginViewSet, base_name='login')

logout_router = routers.SimpleRouter()
logout_router.register('logout', views.LogoutViewSet, base_name='logout')

profile_router = routers.SimpleRouter()
profile_router.register('profiles', views.ProfileViewSet, base_name='profiles')

report_router = routers.SimpleRouter()
report_router.register('reports', views.ReportViewSet, base_name='reports')

review_router = routers.SimpleRouter()
review_router.register('reviews', views.ReviewViewSet, base_name='reviews')

user_router = routers.SimpleRouter()
user_router.register('users', views.UserViewSet, base_name='users')

urlpatterns = []

urlpatterns += find_chat_router.urls
urlpatterns += login_router.urls
urlpatterns += logout_router.urls
urlpatterns += profile_router.urls
urlpatterns += report_router.urls
urlpatterns += review_router.urls
urlpatterns += user_router.urls
