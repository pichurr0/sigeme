# configuration for the chat app that has a route to the consumer

from django.urls import re_path
from . import consumers

# we use re_path() due to limitations in URLRouter.
websocket_urlpatterns = [
    re_path(r"ws/stats/", consumers.Consumer.as_asgi()),
   
]