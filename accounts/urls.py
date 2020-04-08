from django.conf.urls import url
from django.urls import path
from rest_framework_nested import routers

from accounts import views


login_router = routers.SimpleRouter()
login_router.register('login', views.LoginView, basename='login')

logout_router = routers.SimpleRouter()
logout_router.register('logout', views.LogoutView, basename='logout')

opentime_router = routers.SimpleRouter()
opentime_router.register(
    'opentime', views.OpenTimeViewSet, basename='opentime')

profile_router = routers.SimpleRouter()
profile_router.register('profiles', views.ProfileViewSet, basename='profiles')

queue_router = routers.SimpleRouter()
queue_router.register('queue', views.QueueViewSet, basename='queue')

register_router = routers.SimpleRouter()
register_router.register('register', views.RegisterView, basename='register')

report_router = routers.SimpleRouter()
report_router.register('reports', views.ReportViewSet, basename='reports')

review_router = routers.SimpleRouter()
review_router.register('reviews', views.ReviewViewSet, basename='reviews')

talk_router = routers.SimpleRouter()
talk_router.register('talk', views.TalkViewSet, basename='talk')

topic_router = routers.SimpleRouter()
topic_router.register('topics', views.TopicViewSet, basename='topic')

conversation_starter_router = routers.SimpleRouter()
conversation_starter_router.register(
    'conversation-starters', views.ConversationStarterViewSet, basename='conversation_starters')

tips_router = routers.SimpleRouter()
tips_router.register('tips', views.TipsViewSet, basename='tips')

urlpatterns = [
    url(r'^analyze/$', views.Analyze.as_view(), name='analyze')
]

urlpatterns += login_router.urls
urlpatterns += logout_router.urls
urlpatterns += opentime_router.urls
urlpatterns += profile_router.urls
urlpatterns += queue_router.urls
urlpatterns += register_router.urls
urlpatterns += report_router.urls
urlpatterns += review_router.urls
urlpatterns += talk_router.urls
urlpatterns += topic_router.urls
urlpatterns += conversation_starter_router.urls
urlpatterns += tips_router.urls
