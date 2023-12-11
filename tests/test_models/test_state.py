#!/usr/bin/python3
import unittest
import os
from models.state import State
from datetime import datetime
from time import sleep

class TestStateInstantiation(unittest.TestCase):
    """Test cases for the State class instantiation."""

    def test_instantiation_no_args(self):
        """Test State instantiation with no arguments."""
        state = State()
        self.assertEqual(State, type(state)

    def test_new_instance_stored_in_objects(self):
        """Test if a new State instance is stored in the 'objects' dictionary."""
        state = State()
        self.assertIn(state, models.storage.all().values())

    def test_id_is_str(self):
        """Test if the 'id' attribute is a string."""
        state = State()
        self.assertEqual(str, type(state.id))

    def test_created_at_is_datetime(self):
        """Test if 'created_at' is a datetime object."""
        state = State()
        self.assertEqual(datetime, type(state.created_at))

    def test_updated_at_is_datetime(self):
        """Test if 'updated_at' is a datetime object."""
        state = State()
        self.assertEqual(datetime, type(state.updated_at))

    def test_name_is_class_attribute(self):
        """Test if 'name' is a class attribute of the State class."""
        state = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state))
        self.assertNotIn("name", state.__dict__)

    def test_unique_ids(self):
        """Test that two State instances have unique IDs."""
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_different_created_at(self):
        """Test that two State instances have different 'created_at' times."""
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    def test_different_updated_at(self):
        """Test that two State instances have different 'updated_at' times."""
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

    def test_str_representation(self):
        """Test the string representation of a State instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = dt
        state_str = state.__str__()
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + dt_repr, state_str)
        self.assertIn("'updated_at': " + dt_repr, state_str)

    def test_instantiation_with_unused_args(self):
        """Test State instantiation with unused arguments."""
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test State instantiation with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        state = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(state.id, "345")
        self.assertEqual(state.created_at, dt)
        self.assertEqual(state.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test State instantiation with None keyword arguments."""
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

class TestStateSave(unittest.TestCase):
    """Test cases for the save method of the State class."""

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
        """Test saving a State instance once."""
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        self.assertLess(first_updated_at, state.updated_at)

    def test_two_saves(self):
        """Test saving a State instance twice."""
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        second_updated_at = state.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state.save()
        self.assertLess(second_updated_at, state.updated_at)

    def test_save_with_arg(self):
        """Test saving a State instance with an argument."""
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def test_save_updates_file(self):
        """Test if saving a State instance updates the 'file.json' file."""
        state = State()
        state.save()
        state_id = "State." + state.id
        with open("file.json", "r") as f:
            self.assertIn(state_id, f.read())

class TestStateToDict(unittest.TestCase):
    """Test cases for the to_dict method of the State class."""

    def test_to_dict_type(self):
        """Test the type of the 'to_dict' method output."""
        state = State()
        self.assertTrue(dict, type(state.to_dict()))

    def test_to_dict_contains_keys(self):
        """Test if 'to_dict' output contains the expected keys."""
        state = State()
        state_dict = state.to_dict()
        self.assertIn("id", state_dict)
        self.assertIn("created_at", state_dict)
        self.assertIn("updated_at", state_dict)
        self.assertIn("__class__", state_dict)

    def test_to_dict_contains_added_attributes(self):
        """Test if 'to_dict' contains additional attributes added to a State instance."""
        state = State()
        state.middle_name = "Holberton"
        state.my_number = 98
        self.assertEqual("Holberton", state.middle_name)
        self.assertIn("my_number", state.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test if datetime attributes in 'to_dict' are strings."""
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of 'to_dict' against an expected dictionary."""
        dt = datetime.today()
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(state.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test the difference between 'to_dict' and '__dict__'."""
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    def test_to_dict_with_arg(self):
        """Test 'to_dict' method with an argument."""
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)

if __name__ == "__main__":
    unittest.main()
