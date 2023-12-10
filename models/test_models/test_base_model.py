#!/usr/bin/python3
"""Unit tests for your BaseModel class.

Unit test classes:
    TestBaseModelInstantiation
    TestBaseModelSave
    TestBaseModelToDict
"""
import os
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
import models


class TestBaseModelInstantiation(unittest.TestCase):
    """Unit tests for testing instantiation of the BaseModel class."""

    def test_base_model_instantiation(self):
        '''Test if creating an instance of BaseModel works'''
        base_model_instance = BaseModel()
        self.assertIsInstance(base_model_instance, BaseModel)

    def test_new_instance_stored_in_objects(self):
        '''Test if a new instance is stored in the objects dictionary'''
        base_model_instance = BaseModel()
        self.assertIn(base_model_instance, models.storage.all().values())

    def test_id_is_string(self):
        '''Test if the 'id' attribute is a string'''
        base_model_instance = BaseModel()
        self.assertIsInstance(base_model_instance.id, str)

    def test_created_at_is_datetime(self):
        '''Test if the 'created_at' attribute is a datetime object'''
        base_model_instance = BaseModel()
        self.assertIsInstance(base_model_instance.created_at, datetime)

    def test_updated_at_is_datetime(self):
        '''Test if the 'updated_at' attribute is a datetime object'''
        base_model_instance = BaseModel()
        self.assertIsInstance(base_model_instance.updated_at, datetime)

    def test_two_models_have_unique_ids(self):
        '''Test if two BaseModel instances have unique IDs'''
        base_model_instance1 = BaseModel()
        base_model_instance2 = BaseModel()
        self.assertNotEqual(base_model_instance1.id, base_model_instance2.id)

    def test_two_models_have_different_created_at(self):
        '''Test if two BaseModel instances have different 'created_at' timestamps'''
        base_model_instance1 = BaseModel()
        sleep(0.05)
        base_model_instance2 = BaseModel()
        self.assertLess(base_model_instance1.created_at, base_model_instance2.created_at)

    def test_two_models_have_different_updated_at(self):
        '''Test if two BaseModel instances have different 'updated_at' timestamps'''
        base_model_instance1 = BaseModel()
        sleep(0.05)
        base_model_instance2 = BaseModel()
        self.assertLess(base_model_instance1.updated_at, base_model_instance2.updated_at)

    def test_str_representation(self):
        '''Test the string representation of a BaseModel instance'''
        base_model_instance = BaseModel()
        base_model_instance.id = "123456"
        dt = base_model_instance.created_at
        dt_repr = repr(dt)
        base_model_str = str(base_model_instance)
        self.assertIn("[BaseModel] (123456)", base_model_str)
        self.assertIn("'id': '123456'", base_model_str)
        self.assertIn("'created_at': " + dt_repr, base_model_str)

    def test_instantiation_with_args_and_kwargs(self):
        '''Test instantiation with both positional arguments and keyword arguments'''
        dt = datetime.today()
        dt_iso = dt.isoformat()
        base_model_instance = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(base_model_instance.id, "345")
        self.assertEqual(base_model_instance.created_at, dt)
        self.assertEqual(base_model_instance.updated_at, dt)


class TestBaseModelSave(unittest.TestCase):
    """Unit tests for the save method of the BaseModel class."""

    @classmethod
    def setUpClass(cls):
        """Create a backup of the file.json, if it exists."""
        cls.file_path = "file.json"
        cls.backup_path = "file.json.bak"
        if os.path.isfile(cls.file_path):
            os.rename(cls.file_path, cls.backup_path)

    @classmethod
    def tearDownClass(cls):
        """Restore the original file.json if it was backed up."""
        if os.path.isfile(cls.backup_path):
            os.rename(cls.backup_path, cls.file_path)

    def test_save_updates_updated_at(self):
        """Test if the 'save' method updates the 'updated_at' attribute."""
        base_model_instance = BaseModel()
        first_updated_at = base_model_instance.updated_at
        sleep(0.05)
        base_model_instance.save()
        self.assertLess(first_updated_at, base_model_instance.updated_at)

    def test_save_with_argument(self):
        """Test that 'save' method does not accept arguments."""
        base_model_instance = BaseModel()
        with self.assertRaises(TypeError):
            base_model_instance.save(None)

    def test_save_updates_file(self):
        """Test if the 'save' method updates the 'file.json' file."""
        base_model_instance = BaseModel()
        base_model_instance.save()
        base_model_id = "BaseModel." + base_model_instance.id
        with open("file.json", "r") as file:
            self.assertIn(base_model_id, file.read())


class TestBaseModelToDict(unittest.TestCase):
    """Unit tests for the to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        """Test if the 'to_dict' method returns a dictionary."""
        base_model_instance = BaseModel()
        self.assertIsInstance(base_model_instance.to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        """Test if the 'to_dict' method contains the correct keys."""
        base_model_instance = BaseModel()
        self.assertIn("id", base_model_instance.to_dict())
        self.assertIn("created_at", base_model_instance.to_dict())
        self.assertIn("updated_at", base_model_instance.to_dict())
        self.assertIn("__class__", base_model_instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test if the 'to_dict' method includes added attributes."""
        base_model_instance = BaseModel()
        base_model_instance.name = "My Airbnb"
        self.assertIn("name", base_model_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        """Test if the 'created_at' and 'updated_at' values are strings in the dictionary."""
        base_model_instance = BaseModel()
        base_model_dict = base_model_instance.to_dict()
        self.assertEqual(str, type(base_model_dict["created_at"]))
        self.assertEqual(str, type(base_model_dict["updated_at"]))



if __name__ == "__main__":
    unittest.main()

