import os
import json

# from .. import models

BASEPATH = os.path.dirname(os.path.realpath(__file__))


def writeJSONFile(array_or_dict, filename):
    fout = open(f'{BASEPATH}/{filename}', 'w')
    fout.write(json.dumps(array_or_dict, indent=2))
    fout.close()


# Empty garden fixture
garden = [{
    "model": "communitygarden.plot",
    "fields": {
        "grid_x": i,
        "grid_y": j,
        "soil": None,
        "plant": None,
    }
} for i in range(1, 21) for j in range(1, 21)]

writeJSONFile(garden, 'emptygarden.json')

# Species fixture
species_base = [
    ("Rose", "🌹"),
    ("Hibiscus", "🌺"),
    ("Sunflower", "🌻"),
    ("Daisy", "🌼"),
    ("Tulip", "🌷"),
    ("Sprout", "🌱"),
    ("Tree", "🌳"),
    ("Cactus", "🌵"),
    ("Wheat", "🌾"),
    ("Clover", "🍀")
]
species = [{
    "model": "communitygarden.plantspecies",
    "fields": {
        "id": i,
        "name": info[0],
        "emoji": info[1],
    }
} for i, info in enumerate(species_base)]

writeJSONFile(species, 'species.json')


# Test
# allplots = list(models.Plot.objects.all().values())
# writeJSONFile(allplots, 'test.json')
