from django.db import models


class Plot(models.Model):
    """
    plant (?)
    ground type
        --> if soil, soil quality, wetness, fertilization details
        --> else, don't allow plants
    associated history entries?
    """

    grid_x = models.IntegerField()
    grid_y = models.IntegerField()
    plant = models.IntegerField()

    def __str__(self):
        return f'Plot [{str(self.grid_x)}, {str(self.grid_y)}]'
