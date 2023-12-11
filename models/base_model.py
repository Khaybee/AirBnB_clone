#!/usr/bin/python3
'''BaseModel class'''
import uuid
from datetime import datetime
import models


class BaseModel():
    '''A class that defines all common attributes/methods for other classes'''
    def __init__(self, *args, **kwargs):
        '''Initializing the Basemodel.
        Args:
        *args: won’t be used
        **kwargs: dic representation of instance
        '''
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.fromisoformat(value)
                else:
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        '''Returns the string representation of the BaseModel instance'''
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        '''updates the public instance attribute updated_at'''
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        dict_cop = self.__dict__.copy()
        dict_cop["__class__"] = self.__class__.__name__
        dict_cop["created_at"] = self.created_at.isoformat()
        dict_cop["updated_at"] = self.updated_at.isoformat()
        return dict_cop
