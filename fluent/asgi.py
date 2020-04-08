"""
Root router, manages multiple protocols and routes each of them into
appropriate applications.

Exposes a module-level variable named ``application``.
"""
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from fluent.wsgi import application as wsgi_application

from accounts.channels import CallConsumer

asgi_application = URLRouter([
    url(r"^call/(?P<stream>\w+)$", CallConsumer),
])

application = ProtocolTypeRouter({
    'websocket': asgi_application,
    'http': wsgi_application
})
