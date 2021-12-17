# chat/consumers.py
import json
import datetime
from pytz import UTC
from asgiref.sync import async_to_sync as a2s, sync_to_async as s2a
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels_presence.models import Room

from . import models, settings, tasks


# Base consumer classes

class BaseSyncConsumer(WebsocketConsumer):
    def group_send(self, *args, **kwargs):
        return a2s(self.channel_layer.group_send)(self.group_name, *args, **kwargs)

    def group_add(self, *args, **kwargs):
        return Room.objects.add(self.group_name, self.channel_name)

    def group_discard(self, *args, **kwargs):
        return Room.objects.remove(self.group_name, self.channel_name)

    def server_error(self, message):
        self.send(text_data=json.dumps({
            "type": "server_error",
            "message": message,
        }))

    class Meta:
        abstract = True


class BaseAsyncConsumer(AsyncWebsocketConsumer):
    async def group_send(self, *args, **kwargs):
        return await self.channel_layer.group_send(self.group_name, *args, **kwargs)

    async def group_add(self, *args, **kwargs):
        return await s2a(Room.objects.add)(self.group_name, self.channel_name)

    async def group_discard(self, *args, **kwargs):
        return await s2a(Room.objects.remove)(self.group_name, self.channel_name)

    async def server_error(self, message):
        await self.send(text_data=json.dumps({
            "type": "server_error",
            "message": message,
        }))

    class Meta:
        abstract = True


# Consumers

class CursorConsumer(BaseAsyncConsumer):
    group_name = "cursor_group"

    async def connect(self):
        # Generate an ID from the random channel name
        self.client_id = self.channel_name[-10:]

        # Join room (channels_presence handles layer group)
        self.room = await s2a(Room.objects.add)(self.group_name, self.channel_name)
        await self.accept()

        # Notify user of their client id
        await self.group_send({
            "type": "send_cursor_update",
            "client": self.client_id,
            "coords": [0, 0]
        })

    async def disconnect(self, close_code):
        # Leave room group
        await self.group_send({
            "type": "send_cursor_disconnect",
            "client": self.client_id
        })
        await s2a(Room.objects.remove)(self.group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        coords = text_data_json["coords"]

        await self.group_send({
            "type": "send_cursor_update",
            "client": self.client_id,
            "coords": coords,
        })

    # Notify room of cursor_update
    async def send_cursor_update(self, event):
        if self.client_id != event['client']:
            await self.send(text_data=json.dumps({
                'type': 'cursor.update',
                'client': event['client'],
                'coords': event['coords'],
            }))

    # Notify room of cursor_disconnect
    async def send_cursor_disconnect(self, event):
        await self.send(text_data=json.dumps({
            'type': 'cursor.disconnect',
            'client': event['client'],
        }))


class GridConsumer(BaseSyncConsumer):
    group_name = 'grid_group'

    def connect(self):
        # Join room group
        self.room = Room.objects.add(self.group_name, self.channel_name)
        # Accept the connection
        self.accept()
        # Send grid data to the client
        self.send_grid_full_update()

    def disconnect(self, close_code):
        self.group_discard()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print(text_data_json)
        action = text_data_json['action']
        params = text_data_json['params']

        self.update_plot(action, params)

    def send_grid_plot_update(self, event):
        # Notify the client of an update at a single plot
        self.send(text_data=json.dumps({
            'type': 'grid.plotUpdate',
            'plot': event['plot'],
        }))

    def send_grid_full_update(self, event={}):
        # Notify the client to update the whole grid
        plots = [plot.as_dict() for plot in models.Plot.objects.all()]
        self.send(text_data=json.dumps({
            'type': 'grid.fullUpdate',
            'grid': plots
        }))

    def update_plot(self, action, params):
        # Get the data
        plot = models.Plot.objects.get(
            grid_x=params['grid_x'],
            grid_y=params['grid_y']
        )

        print(action)
        # Mutate the data
        if action == 'water':
            if plot.has_soil():
                plot.soil.water_level += 10
                plot.soil.save()
            else:
                return self.server_error(
                    "A plot must have soil in order to be watered."
                )

        elif action == 'dev_dewater':
            if plot.has_soil():
                plot.soil.water_level -= 10
                plot.soil.save()
            else:
                return self.server_error(
                    "A plot must have soil in order to be unwatered."
                )

        elif action == 'soilify':
            if not plot.has_soil():
                plot.soil = models.Soil()
                plot.soil.save()
            else:
                return self.server_error(
                    "There is already soil in this plot."
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
                plot.plant.delete()
                plot.plant = None
            else:
                return self.server_error(
                    "A plot must have soil before a plant can be added."
                )

        elif action == 'dev_removehealth':
            if plot.has_plant():
                plot.plant.health -= 10
            else:
                return self.server_error(
                    "A plot must have a plant in order to affect its health."
                )

        elif action == 'dev_addhealth':
            if plot.has_plant():
                plot.plant.health += 10
            else:
                return self.server_error(
                    "A plot must have a plant in order to affect its health."
                )

        plot.save()

        # Notify all channels of the plot update
        self.group_send({
            'type': 'send_grid_plot_update',
            'plot': plot.as_dict(),
        })

    # def manual_step(self):
    #     tasks.step_once()
