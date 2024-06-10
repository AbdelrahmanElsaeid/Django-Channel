
# Django Channels Chat Application

This is a simple chat application built using Django Channels to enable real-time communication.
## Installation
`python -m pip install -U channels["daphne"]`


```python
INSTALLED_APPS = (
    "daphne",
    ...
)
```

## Configuration

1. Update `settings.py` to include the Channels configuration:
  Add `dephne` to `INSTALLED_APPS` in `settings.py`

```python
   INSTALLED_APPS = [
       ...
       'dephane',
       # Your apps
   ]

   ASGI_APPLICATION = 'yourproject.asgi.application'

   CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
 ```

2. update `asgi.py` to handle both HTTP and WebSocket requests

```python
import os

from django.core.asgi import get_asgi_application


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
             AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
        ),
    }
)
```


## Creating a Chat Consumer

Create a consumer for handling WebSocket connections. Example:

```python
# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Connect code here

    async def disconnect(self, close_code):
        # Disconnect code here

    async def receive(self, text_data):
        # Receive code here

    async def chat_message(self, event):
        # Chat message handling here
```


## URL Routing

Define URL routing for WebSocket connections. Example:

```python
# chat/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
```


