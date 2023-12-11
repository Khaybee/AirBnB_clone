#!/usr/bin/python3
"""__init__ magic method for models directory"""

from models.engine import file_storage
storage = file_storage.FileStorage()
storage.reload()
