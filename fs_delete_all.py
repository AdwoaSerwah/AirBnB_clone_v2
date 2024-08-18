#!/usr/bin/python3
from models import storage

# Get all objects
all_objects = storage.all()

# Clear all objects
for key in list(all_objects.keys()):
    storage.delete(all_objects[key])

# Save changes to persist deletion
storage.save()
