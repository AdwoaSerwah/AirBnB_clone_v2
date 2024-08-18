from models import storage

# Get all objects
all_objects = storage.all()

# Delete all objects
for obj in all_objects.values():
    storage.delete(obj)

# Commit changes to persist deletion
storage.save()
