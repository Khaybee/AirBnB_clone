#!/usr/bin/python3
import unittest
import os
from models.user import User
from datetime import datetime
from time import sleep

class TestUserInstantiation(unittest.TestCase):
    """Test cases for the User class instantiation."""

    def test_instantiation_no_args(self):
        """Test User instantiation with no arguments."""
        user = User()
        self.assertEqual(User, type(user))

    def test_new_instance_stored_in_objects(self):
        """Test if a new User instance is stored in the 'objects' dictionary."""
        user = User()
        self.assertIn(user, models.storage.all().values())

    def test_id_is_str(self):
        """Test if the 'id' attribute is a string."""
        user = User()
        self.assertEqual(str, type(user.id))

    def test_created_at_is_datetime(self):
        """Test if 'created_at' is a datetime object."""
        user = User()
        self.assertEqual(datetime, type(user.created_at))

    def test_updated_at_is_datetime(self):
        """Test if 'updated_at' is a datetime object."""
        user = User()
        self.assertEqual(datetime, type(user.updated_at))

    def test_email_is_str(self):
        """Test if 'email' is a string attribute."""
        user = User()
        self.assertEqual(str, type(user.email))

    def test_password_is_str(self):
        """Test if 'password' is a string attribute."""
        user = User()
        self.assertEqual(str, type(user.password))

    def test_first_name_is_str(self):
        """Test if 'first_name' is a string attribute."""
        user = User()
        self.assertEqual(str, type(user.first_name))

    def test_last_name_is_str(self):
        """Test if 'last_name' is a string attribute."""
        user = User()
        self.assertEqual(str, type(user.last_name))

    def test_unique_ids(self):
        """Test that two User instances have unique IDs."""
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_different_created_at(self):
        """Test that two User instances have different 'created_at' times."""
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_different_updated_at(self):
        """Test that two User instances have different 'updated_at' times."""
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_str_representation(self):
        """Test the string representation of a User instance."""
        dt = datetime.today()
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        user_str = user.__str__()
        self.assertIn("[User] (123456)", user_str)
        self.assertIn("'id': '123456'", user_str)
        self.assertIn("'created_at': " + repr(dt), user_str)
        self.assertIn("'updated_at': " + repr(dt), user_str)

    def test_instantiation_with_unused_args(self):
        """Test User instantiation with unused arguments."""
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test User instantiation with keyword arguments."""
        dt = datetime.today()
        user = User(id="345", created_at=dt, updated_at=dt)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test User instantiation with None keyword arguments."""
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

class TestUserSave(unittest.TestCase):
    """Test cases for the save method of the User class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Test saving a User instance once."""
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def test_two_saves(self):
        """Test saving a User instance twice."""
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        second_updated_at = user.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        user.save()
        self.assertLess(second_updated_at, user.updated_at)

    def test_save_with_arg(self):
        """Test saving a User instance with an argument."""
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def test_save_updates_file(self):
        """Test if saving a User instance updates the 'file.json' file."""
        user = User()
        user.save()
        user_id = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(user_id, f.read())

class TestUserToDict(unittest.TestCase):
    """Test cases for the to_dict method of the User class."""

    def test_to_dict_type(self):
        """Test the type of the 'to_dict' method output."""
        user = User()
        self.assertTrue(dict, type(user.to_dict()))

    def test_to_dict_contains_keys(self):
        """Test if 'to_dict' output contains the expected keys."""
        user = User()
        user_dict = user.to_dict()
        self.assertIn("id", user_dict)
        self.assertIn("created_at", user_dict)
        self.assertIn("updated_at", user_dict)
        self.assertIn("__class__", user_dict)

    def test_to_dict_contains_added_attributes(self):
        """Test if 'to_dict' contains additional attributes added to a User instance."""
        user = User()
        user.middle_name = "Holberton"
        user.my_number = 98
        self.assertEqual("Holberton", user.middle_name)
        self.assertIn("my_number", user.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test if datetime attributes in 'to_dict' are strings."""
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(str, type(user_dict["id"]))
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of 'to_dict' against an expected dictionary."""
        dt = datetime.today()
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(user.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test the difference between 'to_dict' and '__dict__'."""
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def test_to_dict_with_arg(self):
        """Test 'to_dict' method with an argument."""
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)

if __name__ == "__main__":
    unittest.main()
