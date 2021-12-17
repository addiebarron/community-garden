from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from .utils import clamp, print_in_main_process as log


class CleanModel(models.Model):
    """
    A base model class for self-validating and -normalizing models.
    Runs clean() and clean_fields() before calling save().
    """

    def save(self, *args, **kwargs):
        # Clean first, to normalize values if needed
        # Now validate data
        try:
            self.clean()
            self.clean_fields()
            self.validate_unique()
        except ValidationError as e:
            print(e)
        finally:
            super(CleanModel, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        super(CleanModel, self).clean(*args, **kwargs)

    class Meta:
        abstract = True


class Disconnection(models.Model):
    """
    Table containing information about the last
    disconnection from the app.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    # Store only the last 10 connections
    def save(self, *args, **kwargs):
        objects = Disconnection.objects.order_by('timestamp')
        count = objects.count()
        limit = 10
        if count >= limit:
            [obj.delete() for obj in objects[0:count-limit+1]]

        super(Disconnection, self).save(*args, **kwargs)


class Plot(CleanModel):
    """
    grid position
    soil (optional)
        --> else, don't allow plants
    plant (optional)
    //
    associated history entries
    """

    grid_x = models.IntegerField()
    grid_y = models.IntegerField()
    soil = models.OneToOneField(
        'Soil',
        on_delete=models.CASCADE,
        related_name="plot_in",
        blank=True,
        null=True
    )
    plant = models.OneToOneField(
        'Plant',
        on_delete=models.CASCADE,
        related_name="plot_in",
        blank=True,
        null=True,
    )
    # last_edited = models.DateTimeField()

    class Meta:
        unique_together = ('grid_x', 'grid_y')

    def has_soil(self):
        return isinstance(self.soil, Soil)

    def has_plant(self):
        return isinstance(self.plant, Plant)

    def save(self, *args, **kwargs):
        """
        Wrapper for the default save method.
        Saves any existing child objects (plant, soil).
        Child objects should all inherit from CleanModel, so 
        they'll have their fields validated before saving.
        """
        if self.has_soil():
            self.soil.save()
        if self.has_plant():
            self.plant.save()

        super(Plot, self).save(*args, **kwargs)

    def step(self, *args, **kwargs):
        """
        One time step for a plot.
        Runs a single step for any child objects.
        """
        do_save = False
        if self.has_soil():
            do_save = True
            self.soil.step()
        if self.has_plant():
            do_save = True
            self.plant.step()
        if do_save:
            self.save()

    def __str__(self):
        return f'Plot[{str(self.grid_x)}, {str(self.grid_y)}]'

    def as_dict(self):
        soil = self.soil.as_dict() if self.has_soil() else None
        plant = self.plant.as_dict() if self.has_plant() else None

        return {
            "grid_x": self.grid_x,
            "grid_y": self.grid_y,
            "soil": soil,
            "plant": plant,
        }


class Soil(CleanModel):
    """
    A single instance of soil in a plot.
    water level
    //
    soil type
    nutrient levels, npk
    """
    MIN_WATER_LEVEL = 0
    MAX_WATER_LEVEL = 100

    water_level = models.SmallIntegerField(
        default=50,
        validators=[
            MinValueValidator(MIN_WATER_LEVEL),
            MaxValueValidator(MAX_WATER_LEVEL),
        ]
    )

    # soil_type = models.TextField(choices=[
    #     ("SAND", 4),
    #     ("SILT", 3),
    #     ("LOAM", 2),
    #     ("CLAY", 1),
    # ])

    def clean(self, *args, **kwargs):
        # Clamp the water level
        self.water_level = clamp(
            self.water_level, self.MIN_WATER_LEVEL, self.MAX_WATER_LEVEL)
        super(Soil, self).clean(*args, **kwargs)

    def step(self):
        """
        One time step for the soil.

        Only called from within Plot.save
        Plot.save also handles calling Soil.save
        """
        self.water_level -= 1

    def __str__(self):
        return f'Soil in: {self.plot_in}'

    def as_dict(self):
        return {
            "water_level": self.water_level
        }


class Plant(CleanModel):
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

    species = models.ForeignKey('PlantSpecies', on_delete=models.CASCADE)
    health = models.SmallIntegerField(
        default=100,
        validators=[
            MinValueValidator(MIN_HEALTH),
            MaxValueValidator(MAX_HEALTH),
        ]
    )

    def step(self):
        """
        One time step for a plant.
        Only called from within Plot.save
        """
        if self.plot_in.soil.water_level <= 5:
            log(f'{self.species} on {self.plot_in} has lost 1 health. Now {self.health}.')
            self.health -= 1
        elif self.health <= 0:
            log(f'{self.species} on {self.plot_in} has died.')
            # TODO make this work!
            self.plot_in.plant = None
            self.delete()

    def clean(self, *args, **kwargs):
        self.health = clamp(
            self.health, self.MIN_HEALTH, self.MAX_HEALTH)
        super(Plant, self).clean(*args, **kwargs)

    def __str__(self):
        return f'{self.species} in: {self.plot_in}'

    def as_dict(self):
        return {
            "species": self.species.as_dict(),
            "health": self.health,
        }


class PlantSpecies(models.Model):
    """
    A species of plant.
    """
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    emoji = models.TextField()

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "emoji": self.emoji,
        }


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
