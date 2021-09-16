# chat/consumers.py
import json
from asgiref.sync import async_to_sync as a2s
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from . import models


class BaseConsumer(WebsocketConsumer):
    def group_send(self, *args, **kwargs):
        return a2s(self.channel_layer.group_send)(self.group_name, *args, **kwargs)

    def group_add(self, *args, **kwargs):
        return a2s(self.channel_layer.group_add)(self.group_name, self.channel_name)

    def group_discard(self, *args, **kwargs):
        return a2s(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def server_error(self, message):
        self.send({
            "type": "server_error",
            "message": message,
        })


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


class GridConsumer(BaseConsumer):
    group_name = 'grid_group'

    def connect(self):
        # Join room group
        self.group_add()
        # Accept the connection
        self.accept()
        # Send grid data to the client
        self.send_grid_populate()

    def disconnect(self, close_code):
        self.group_discard()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message_type = text_data_json['type']

        # if message_type == 'update':
        self.update_plot(text_data_json)

    def update_plot(self, text_data_json):
        action = text_data_json['action']
        params = text_data_json['params']

        plot = models.Plot.objects.get(
            grid_x=params['grid_x'],
            grid_y=params['grid_y']
        )

        if action == 'water':
            if plot.has_soil():
                plot.soil.water_level = min(
                    plot.soil.water_level + 3,  # TODO slightly random
                    models.Soil.MAX_WATER_LEVEL
                )
                plot.soil.save()
            else:
                return self.server_error(
                    "A plot must have soil in order to be watered."
                )

        elif action == 'soilify':
            if not plot.has_soil():
                plot.soil = models.Soil()
                plot.soil.save()
            else:
                return self.server_error(
                    "There is already soil in this plot."
                )

        elif action == 'plant':
            if plot.has_soil():
                if not plot.has_plant():
                    plant_id = params["id"]
                    # species = models.Species.get(name=params["name"])
                    species = models.PlantSpecies.objects.get(id=plant_id)
                    plot.plant = models.Plant(species=species)
                    plot.plant.save()
                else:
                    return self.server_error(
                        "Cannot plant in the same plot as another plant."
                    )
            else:
                return self.server_error(
                    "A plot must have soil before a plant can be added."
                )

        elif action == 'uproot':
            if plot.has_plant():
                models.Plant.objects.get(id=plot.plant.id).delete()
                plot.plant = None
            else:
                return self.server_error(
                    "A plot must have soil before a plant can be added."
                )

        elif action == 'desoilify':
            if plot.has_soil():
                if not plot.has_plant():
                    models.Soil.objects.get(id=plot.soil.id).delete()
                    plot.soil = None
                else:
                    return self.server_error(
                        "Soil cannot be removed if there's a plant."
                    )
            else:
                return self.server_error(
                    "There is no soil to remove."
                )

        plot.full_clean()
        plot.save()

        self.group_send({
            'type': 'send_grid_update',
            'grid_x': params['grid_x'],
            'grid_y': params['grid_y'],
            'plot': plot.as_dict(),
        })

    def send_grid_update(self, event):
        # Push changes to all connected clients
        self.send(text_data=json.dumps({
            'type': 'grid_update',
            'grid_x': event['grid_x'],
            'grid_y': event['grid_y'],
            'plot': event['plot'],
        }))

    def send_grid_populate(self):
        plots = [plot.as_dict() for plot in models.Plot.objects.all()]
        self.send(text_data=json.dumps({
            'type': 'grid_populate',
            'data': plots
        }))
