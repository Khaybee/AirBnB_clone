#!/usr/bin/python3
"""The Amenity class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Representing an amenity.

    Attributes:
        name (str): The name of the amenity.
    """
    name = ""
