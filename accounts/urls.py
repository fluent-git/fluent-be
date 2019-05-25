from django.conf.urls import url
from django.urls import path
from rest_framework_nested import routers

from accounts import views

user_router = routers.SimpleRouter()
user_router.register('users', views.UserViewSet, base_name='users')

urlpatterns = []
urlpatterns += user_router.urls
