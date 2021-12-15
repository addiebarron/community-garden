# Tasks for django-workers

from workers import task
from .models import Plot
from .utils import print_in_main_process
from .settings import GROWTH_RATE


@task(schedule=GROWTH_RATE)
def step_once():
    print_in_main_process(
        f"This should happen every {str(GROWTH_RATE)} seconds")
    # for plot in Plot.objects.all():
    #     plot.step()
