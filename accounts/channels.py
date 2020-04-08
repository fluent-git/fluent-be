from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer

class CallConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })
        self.send({
            "type": "websocket.send",
            "text": self.scope["url_route"]["kwargs"]["stream"],
        })

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": event["text"],
        })

    def websocket_disconnect(self, event):
        raise StopConsumer