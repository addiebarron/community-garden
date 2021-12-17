import os
import json

# from .. import models

BASEPATH = os.path.dirname(os.path.realpath(__file__))
data = []

# Empty garden fixture
data += [{
    "model": "communitygarden.plot",
    "fields": {
        "grid_x": i,
        "grid_y": j,
        "soil": None,
        "plant": None,
    }
} for i in range(1, 21) for j in range(1, 21)]

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
data += [{
    "model": "communitygarden.plantspecies",
    "fields": {
        "id": i,
        "name": info[0],
        "emoji": info[1],
    }
} for i, info in enumerate(species_base)]

fout = open(f'{BASEPATH}/data.json', 'w')
fout.write(json.dumps(data, indent=2))
fout.close()

# Test
# allplots = list(models.Plot.objects.all().values())
# writeJSONFile(allplots, 'test.json')
