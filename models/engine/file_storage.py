#!/usr/bin/python3
"""the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage():
    """Representing an abstract storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return self.__objects
    
    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        key_name = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key_name] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        with open(self.__file_path, 'w') as f:
            dic = {key : value.to_dict() for key, value in self.__objects.items()}
            json.dump(dic, f)
    
    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(self.__file_path, "r") as f:
                obj_dict = json.load(f)
                for object_value in obj_dict.values():
                    class_name = object_value["__class__"]
                    del object_value["__class__"]
                    self.new(eval(f"{class_name}")(**object_value))
        except FileNotFoundError:
            pass
