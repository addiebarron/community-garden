from django.db import models as m
from django.core.validators import MaxValueValidator, MinValueValidator


class Connection(m.Model):
    """
    Table containing information about the history of
    connections to the app.
    """
    timestamp = m.DateTimeField(auto_now_add=True)

    # Store only the last 10 connections
    def save(self, *args, **kwargs):
        objects = Connection.objects.order_by('timestamp')
        count = objects.count()
        limit = 10
        if count >= limit:
            [obj.delete() for obj in objects[0:count-limit+1]]

        super(Connection, self).save(*args, **kwargs)


class Plot(m.Model):
    """
    grid position
    soil (optional)
        --> else, don't allow plants
    plant (optional)
    //
    associated history entries
    """

    grid_x = m.IntegerField()
    grid_y = m.IntegerField()
    soil = m.OneToOneField(
        'Soil',
        on_delete=m.CASCADE,
        related_name="plot_in",
        blank=True,
        null=True
    )
    plant = m.OneToOneField(
        'Plant',
        on_delete=m.CASCADE,
        related_name="plot_in",
        blank=True,
        null=True,
    )
    # last_edited = m.DateTimeField()

    def has_soil(self):
        return isinstance(self.soil, Soil)

    def has_plant(self):
        return isinstance(self.plant, Plant)

    def __str__(self):
        return f'Plot at [{str(self.grid_x)}, {str(self.grid_y)}]'

    def as_dict(self):
        soil = self.soil.as_dict() if self.has_soil() else None
        plant = self.plant.as_dict() if self.has_plant() else None

        return {
            "grid_x": self.grid_x,
            "grid_y": self.grid_y,
            "soil": soil,
            "plant": plant,
        }


class Soil(m.Model):
    """
    A single instance of soil in a plot.
    water level
    //
    soil type
    nutrient levels, npk
    """
    MIN_WATER_LEVEL = 1
    MAX_WATER_LEVEL = 100
    # soil_type = m.TextField(choices=[
    #     ("SAND", 4),
    #     ("SILT", 3),
    #     ("LOAM", 2),
    #     ("CLAY", 1),
    # ])
    water_level = m.SmallIntegerField(
        default=50,
        validators=[
            MinValueValidator(MIN_WATER_LEVEL),
            MaxValueValidator(MAX_WATER_LEVEL),
        ]
    )

    def __str__(self):
        return f'Soil in plot: {self.plot_in}'

    def as_dict(self):
        return {
            "water_level": self.water_level
        }


class Plant(m.Model):
    """
    A single instance of a plant in a plot.
    species
    health
    //
    current pests
    flowers
    fruit
    """
    MIN_HEALTH = 0
    MAX_HEALTH = 100

    species = m.ForeignKey('PlantSpecies', on_delete=m.CASCADE)
    health = m.SmallIntegerField(
        default=100,
        validators=[
            MinValueValidator(MIN_HEALTH),
            MaxValueValidator(MAX_HEALTH),
        ]
    )

    def __str__(self):
        return f'{self.species} in plot: {self.plot_in}'

    def as_dict(self):
        return {
            "species": self.species.as_dict(),
            "health": self.health,
        }


class PlantSpecies(m.Model):
    """
    A species of plant.
    """
    id = m.IntegerField(primary_key=True)
    name = m.TextField()
    emoji = m.TextField()

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "emoji": self.emoji,
        }


# class HistoryEntry(m.Model):
    """
    An entry in the history of the garden. Contains information about
    the user, the action taken, the action target, and a timestamp/

    timestamp
    user
    action
    plot location
    frozen plot information at timestamp
    """
