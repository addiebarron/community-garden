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
    # plant = models.ForeignKey('PlantModel', on_delete=models.CASCADE)
    # last_edited = models.DateTimeField()

    def __str__(self):
        return f'Plot [{str(self.grid_x)}, {str(self.grid_y)}]'

# class Plant(models.Model):
#     """
#     age
#     type
#     (other properties determined by type)
#     pests?
#     """
#     name = models.TextField()


# class HistoryEntry(models.Model):
#     """
#     user:
#     action: (actiontaken, target) or just string
#     timestamp: datetime
#     """
