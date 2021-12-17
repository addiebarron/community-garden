# Tasks for django-workers

from workers import task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Plot
from .utils import print_in_main_process
from .settings import GROWTH_RATE


@task(schedule=GROWTH_RATE)
def step_once():

    for plot in Plot.objects.all():
        plot.step()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'grid_group', {'type': 'send_grid_full_update'}
    )
