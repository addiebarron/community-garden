# chat/consumers.py
import json
import datetime
from pytz import UTC
from asgiref.sync import async_to_sync as a2s, sync_to_async as s2a
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels_presence.models import Room

from . import models, settings, tasks


# Base classes

class BaseSyncConsumer(WebsocketConsumer):
    def group_send(self, *args, **kwargs):
        return a2s(self.channel_layer.group_send)(self.group_name, *args, **kwargs)

    def group_add(self, *args, **kwargs):
        return Room.objects.add(self.group_name, self.channel_name)

    def group_discard(self, *args, **kwargs):
        return Room.objects.remove(self.group_name, self.channel_name)

    def server_error(self, message):
        self.send({
            "type": "server_error",
            "message": message,
        })


class BaseAsyncConsumer(AsyncWebsocketConsumer):
    async def group_send(self, *args, **kwargs):
        return await self.channel_layer.group_send(self.group_name, *args, **kwargs)

    async def group_add(self, *args, **kwargs):
        return await s2a(Room.objects.add)(self.group_name, self.channel_name)

    async def group_discard(self, *args, **kwargs):
        return await s2a(Room.objects.remove)(self.group_name, self.channel_name)

    async def server_error(self, message):
        await self.send({
            "type": "server_error",
            "message": message,
        })


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
        await s2a(Room.objects.remove)(self.group_name, self.channel_name)

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


class GridConsumer(BaseSyncConsumer):
    group_name = 'grid_group'

    def connect(self):
        # Join room group
        self.room = Room.objects.add(self.group_name, self.channel_name)
        # Accept the connection
        self.accept()
        # Update the grid based on the last time someone logged in
        self.calculate_growth()
        # Send grid data to the client
        self.send_grid_populate()

    def disconnect(self, close_code):
        self.group_discard()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message_type = text_data_json['type']

        # if message_type == 'update':
        self.update_plot(text_data_json)

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

    def group_send_plot_update(self, plot):
        self.group_send({
            'type': 'send_grid_update',
            'grid_x': plot.grid_x,
            'grid_y': plot.grid_y,
            'plot': plot.as_dict(),
        })

    def update_plot(self, text_data_json):
        action = text_data_json['action']
        params = text_data_json['params']

        # Get the data
        plot = models.Plot.objects.get(
            grid_x=params['grid_x'],
            grid_y=params['grid_y']
        )

        # Mutate the data
        if action == 'water':
            if plot.has_soil():
                plot.soil.water_level = min(
                    plot.soil.water_level + 10,  # TODO slightly random
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
                models.Plant.objects.get(id=plot.plant.id).delete()
                plot.plant = None
            else:
                return self.server_error(
                    "A plot must have soil before a plant can be added."
                )

        # Validate and write to the db
        plot.full_clean()
        plot.save()

        # Notify other users of the plot update
        self.group_send_plot_update(plot)

    def save_disconnect(self):
        # TODO add logic to detect when last client has disconnected
        # --> django-channels-presence package?
        print('Last client disconnecting -- saving disconnect')
        models.Disconnection().save()

    def manual_step(self):
        tasks.step_once()
        # now = datetime.datetime.now(tz=UTC)
        # if models.Disconnection.objects.count() > 0:
        #     # Get time since the last disconnection
        #     last_disconnect = models.Disconnection.objects.latest(
        #         'timestamp').timestamp

        #     # If no one has disconnected since the last disconnect, don't grow
        #     if last_disconnect.used:
        #         return

        #     # Calculate the number of times the garden should have grown
        #     seconds_since_last_disconnect = (now - last_disconnect).seconds
        #     n = int(seconds_since_last_disconnect //
        #             (86400/settings.GROWTH_RATE))

        #     # Mark the last disconnection as used
        #     last_disconnect.update(used=True)

        #     # Run the grow function n times
        #     print("--- NEW CONNECTION -- GROWTH ---")
        #     print(seconds_since_last_disconnect,
        #           "seconds since last connection.")
        #     print("Growing garden", n, "times.")
        #     print("--------------------------------")

        #     plots = models.Plot.objects.all()
        #     for _ in range(n):
        #         for plot in plots:
        #             if plot.has_soil() and plot.soil.water_level > 0:
        #                 plot.soil.water_level -= 1
        #                 plot.save()
