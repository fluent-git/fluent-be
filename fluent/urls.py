from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Fluent API Documentation')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    url(r'documentation', schema_view),
]
