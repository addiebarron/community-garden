# chat/consumers.py
import json
from asgiref.sync import async_to_sync as a2s
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from . import models


class CursorConsumer(AsyncWebsocketConsumer):
    group_name = "cursor_group"

    async def connect(self):
        self.client_id = self.channel_name[-10:]

        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Notify user of their client id
        await self.send(text_data=json.dumps({
            "type": "cursor_connected",
            "client": self.client_id
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_send(
            self.group_name, {
                "type": "send_cursor_disconnected",
                "client": self.client_id
            })
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        coords = text_data_json["coords"]

        # Forward the data to the rest of the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_cursor_update",
                "client": self.client_id,
                "coords": coords,
            },
        )

    # Notify room of cursor_update
    async def send_cursor_update(self, event):
        if self.client_id != event['client']:
            await self.send(text_data=json.dumps({
                'type': 'cursor_update',
                'client': event['client'],
                'coords': event['coords'],
            }))

    # Notify room of cursor_disconnect
    async def send_cursor_disconnected(self, event):

        await self.send(text_data=json.dumps({
            'type': 'cursor_disconnected',
            'client': event['client'],
        }))


class GridConsumer(WebsocketConsumer):
    group_name = 'grid_group'

    def connect(self):
        # Join room group
        a2s(self.channel_layer.group_add)(self.group_name, self.channel_name)
        # Accept the connection
        self.accept()
        # Notify?
        # Send all context data here? Or make separate DRF view for initial connect?
        plots = list(models.Plot.objects.all().values())
        self.send(text_data=json.dumps(
            {'type': 'grid_populate', 'data': plots}))
        # await self.send(text_data=json.dumps({"type": "grid_connected"}))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        if message_type == 'update':
            print('received plant update message:', text_data_json)
            self.update_plot(text_data_json)

    def update_plot(self, text_data_json):
        action = text_data_json['action']
        params = text_data_json['params']

        plot = models.Plot.objects.get(
            grid_x=params['grid_x'],
            grid_y=params['grid_y']
        )

        new_plant = plot.plant

        if action == 'increment_plant':
            new_plant = (new_plant + 1) % 10

        if new_plant != plot.plant:
            plot.plant = new_plant
            plot.save()

            a2s(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_grid_update',
                    'grid_x': params['grid_x'],
                    'grid_y': params['grid_y'],
                    'plant': plot.plant,
                }
            )

    def disconnect(self, close_code):
        a2s(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def send_grid_update(self, event):
        # Push changes to all connected clients
        self.send(text_data=json.dumps({
            'type': 'grid_update',
            'grid_x': event['grid_x'],
            'grid_y': event['grid_y'],
            'plant': event['plant'],
        }))
