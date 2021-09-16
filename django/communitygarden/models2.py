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
    # plant = models.IntegerField()
    soil = models.ForeignKey('Soil', on_delete=models.CASCADE)
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE)
    # last_edited = models.DateTimeField()

    def __str__(self):
        return f'Plot [{str(self.grid_x)}, {str(self.grid_y)}]'


class Soil(models.Model):
    """
    A single instance of soil in a plot.
    """


class Plant(models.Model):
    """
    A single instance of a plant in a plot.
    age
    type
    (other properties determined by type)
    pests?
    """
    species = models.ForeignKey('PlantSpecies', on_delete=models.CASCADE)
    health = models.IntegerField()


class PlantSpecies(models.Model):
    """
    A species of plant.
    """
    name = models.TextField()


# class HistoryEntry(models.Model):
    """
    An entry in the history of the garden. Contains information about 
    the user, the action taken, the action target, and a timestamp/

    timestamp
    user
    action
    plot location
    frozen plot information at timestamp
    """
