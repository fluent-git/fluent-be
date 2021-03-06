from django.conf.urls import url
from django.urls import path
from rest_framework_nested import routers

from accounts import views


login_router = routers.SimpleRouter()
login_router.register('login', views.LoginView, base_name='login')

logout_router = routers.SimpleRouter()
logout_router.register('logout', views.LogoutView, base_name='logout')

opentime_router = routers.SimpleRouter()
opentime_router.register(
    'opentime', views.OpenTimeViewSet, base_name='opentime')

profile_router = routers.SimpleRouter()
profile_router.register('profiles', views.ProfileViewSet, base_name='profiles')

queue_router = routers.SimpleRouter()
queue_router.register('queue', views.QueueViewSet, base_name='queue')

register_router = routers.SimpleRouter()
register_router.register('register', views.RegisterView, base_name='register')

report_router = routers.SimpleRouter()
report_router.register('reports', views.ReportViewSet, base_name='reports')

review_router = routers.SimpleRouter()
review_router.register('reviews', views.ReviewViewSet, base_name='reviews')

talk_router = routers.SimpleRouter()
talk_router.register('talk', views.TalkViewSet, base_name='talk')

topic_router = routers.SimpleRouter()
topic_router.register('topics', views.TopicViewSet, base_name='topic')

conversation_starter_router = routers.SimpleRouter()
conversation_starter_router.register(
    'conversation-starters', views.ConversationStarterViewSet, base_name='conversation_starters')

tips_router = routers.SimpleRouter()
tips_router.register('tips', views.TipsViewSet, base_name='tips')

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
