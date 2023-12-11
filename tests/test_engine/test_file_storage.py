#!/usr/bin/python3
import unittest
import os
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review

class TestFileStorage(unittest.TestCase):
    """Test cases for the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level resources before running any tests."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Clean up class-level resources after running all tests."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_instantiation(self):
        """Test FileStorage instantiation with and without arguments."""
        file_storage = FileStorage()
        self.assertIsInstance(file_storage, FileStorage)
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_private_attributes(self):
        """Test if __file_path and __objects are private attributes."""
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_initialized(self):
        """Test if models.storage is correctly initialized."""
        storage = models.storage
        self.assertIsInstance(storage, FileStorage)

    def test_all_method(self):
        """Test the all() method to ensure it returns a dictionary."""
        all_objects = models.storage.all()
        self.assertIsInstance(all_objects, dict)

    def test_all_method_with_argument(self):
        """Test all() method with an argument to ensure it raises a TypeError."""
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_method(self):
        """Test the new() method by creating and adding objects."""
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        all_objects = models.storage.all()
        self.assertIn(f"BaseModel.{bm.id}", all_objects.keys())
        self.assertIn(bm, all_objects.values())
        self.assertIn(f"User.{us.id}", all_objects.keys())
        self.assertIn(us, all_objects.values())
        self.assertIn(f"State.{st.id}", all_objects.keys())
        self.assertIn(st, all_objects.values())
        self.assertIn(f"Place.{pl.id}", all_objects.keys())
        self.assertIn(pl, all_objects.values())
        self.assertIn(f"City.{cy.id}", all_objects.keys())
        self.assertIn(cy, all_objects.values())
        self.assertIn(f"Amenity.{am.id}", all_objects.keys())
        self.assertIn(am, all_objects.values())
        self.assertIn(f"Review.{rv.id}", all_objects.keys())
        self.assertIn(rv, all_objects.values())

    def test_new_method_with_args(self):
        """Test new() method with arguments to ensure it raises a TypeError."""
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save_method(self):
        """Test the save() method to ensure it correctly saves objects to a file."""
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn(f"BaseModel.{bm.id}", save_text)
            self.assertIn(f"User.{us.id}", save_text)
            self.assertIn(f"State.{st.id}", save_text)
            self.assertIn(f"Place.{pl.id}", save_text)
            self.assertIn(f"City.{cy.id}", save_text)
            self.assertIn(f"Amenity.{am.id}", save_text)
            self.assertIn(f"Review.{rv.id}", save_text)

    def test_save_method_with_argument(self):
        """Test save() method with an argument to ensure it raises a TypeError."""
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_method(self):
        """Test the reload() method to ensure it correctly reloads objects from a file."""
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        reloaded_objects = FileStorage._FileStorage__objects
        self.assertIn(f"BaseModel.{bm.id}", reloaded_objects)
        self.assertIn(f"User.{us.id}", reloaded_objects)
        self.assertIn(f"State.{st.id}", reloaded_objects)
        self.assertIn(f"Place.{pl.id}", reloaded_objects)
        self.assertIn(f"City.{cy.id}", reloaded_objects)
        self.assertIn(f"Amenity.{am.id}", reloaded_objects)
        self.assertIn(f"Review.{rv.id}", reloaded_objects)

    def test_reload_method_with_argument(self):
        """Test reload() method with an argument to ensure it raises a TypeError."""
        with self.assertRaises(TypeError):
            models.storage.reload(None)

if __name__ == "__main__":
    unittest.main()

