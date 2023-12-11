#!/usr/bin/python3
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity

class TestAmenityInstantiation(unittest.TestCase):
    """Unit tests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        """Test that an Amenity instance can be created with no arguments."""
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        """Test that a new Amenity instance is stored in the objects dictionary."""
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test that the 'id' attribute of Amenity is a string."""
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        """Test that the 'created_at' attribute of Amenity is a datetime object."""
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test that the 'updated_at' attribute of Amenity is a datetime object."""
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        """Test that 'name' is a class attribute of Amenity."""
        amenity = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amenity.__dict__)

    def test_two_amenities_unique_ids(self):
        """Test that two Amenity instances have unique IDs."""
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_two_amenities_different_created_at(self):
        """Test that two Amenity instances have different 'created_at' timestamps."""
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_two_amenities_different_updated_at(self):
        """Test that two Amenity instances have different 'updated_at' timestamps."""
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_str_representation(self):
        """Test the string representation of an Amenity instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dt
        amenity_str = amenity.__str__()
        self.assertIn("[Amenity] (123456)", amenity_str)
        self.assertIn("'id': '123456'", amenity_str)
        self.assertIn("'created_at': " + dt_repr, amenity_str)
        self.assertIn("'updated_at': " + dt_repr, amenity_str)

    def test_args_unused(self):
        """Test that passing None as an argument does not affect the Amenity instance."""
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of Amenity with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amenity = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity.id, "345")
        self.assertEqual(amenity.created_at, dt)
        self.assertEqual(amenity.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test that passing None as keyword arguments raises a TypeError."""
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

class TestAmenitySave(unittest.TestCase):
    """Unit tests for testing the save method of the Amenity class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp", "file.json")
        except FileNotFoundError:
            pass

    def test_one_save(self):
        """Test that calling save updates the 'updated_at' timestamp."""
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        self.assertLess(first_updated_at, amenity.updated_at)

    def test_two_saves(self):
        """Test that calling save multiple times updates the 'updated_at' timestamp."""
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        second_updated_at = amenity.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity.save()
        self.assertLess(second_updated_at, amenity.updated_at)

    def test_save_with_arg(self):
        """Test that passing an argument to save raises a TypeError."""
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.save(None)

    def test_save_updates_file(self):
        """Test that calling save updates the file.json storage file."""
        amenity = Amenity()
        amenity.save()
        amenity_id = "Amenity." + amenity.id
        with open("file.json", "r") as f:
            self.assertIn(amenity_id, f.read())

class TestAmenityToDict(unittest.TestCase):
    """Unit tests for testing the to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        """Test the type of the output of to_dict method."""
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the to_dict output contains the correct keys."""
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that to_dict includes attributes added at runtime."""
        amenity = Amenity()
        amenity.middle_name = "Holberton"
        amenity.my_number = 98
        self.assertEqual("Holberton", amenity.middle_name)
        self.assertIn("my_number", amenity.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that the datetime attributes in to_dict are strings."""
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(str, type(amenity_dict["id"]))
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict method."""
        dt = datetime.today()
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dt
        t_dict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(amenity.to_dict(), t_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test the contrast between to_dict and __dict__."""
        amenity = Amenity()
        self.assertNotEqual(amenity.to_dict(), amenity.__dict__)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to to_dict raises a TypeError."""
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict(None)

if __name__ == "__main__":
    unittest.main()

