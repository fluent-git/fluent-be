from django.conf.urls import url
from django.urls import path
from rest_framework_nested import routers

from accounts import views

user_router = routers.SimpleRouter()
user_router.register('users', views.UserViewSet, base_name='users')

login_router = routers.SimpleRouter()
login_router.register('login', views.LoginViewSet, base_name='login')

logout_router = routers.SimpleRouter()
logout_router.register('logout', views.LogoutViewSet, base_name='logout')

urlpatterns = []
urlpatterns += login_router.urls
urlpatterns += logout_router.urls
urlpatterns += user_router.urls
