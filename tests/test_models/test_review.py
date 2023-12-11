#!/usr/bin/python3
import unittest
import os
from models.review import Review
from datetime import datetime
from time import sleep

class TestReviewInstantiation(unittest.TestCase):
    """Test cases for the Review class instantiation."""

    def test_instantiation_no_args(self):
        """Test Review instantiation with no arguments."""
        review = Review()
        self.assertEqual(Review, type(review))

    def test_new_instance_stored_in_objects(self):
        """Test if a new Review instance is stored in the 'objects' dictionary."""
        review = Review()
        self.assertIn(review, models.storage.all().values())

    def test_id_is_str(self):
        """Test if the 'id' attribute is a string."""
        review = Review()
        self.assertEqual(str, type(review.id))

    def test_created_at_is_datetime(self):
        """Test if 'created_at' is a datetime object."""
        review = Review()
        self.assertEqual(datetime, type(review.created_at))

    def test_updated_at_is_datetime(self):
        """Test if 'updated_at' is a datetime object."""
        review = Review()
        self.assertEqual(datetime, type(review.updated_at))

    def test_place_id_is_class_attribute(self):
        """Test if 'place_id' is a class attribute of the Review class."""
        review = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(review))
        self.assertNotIn("place_id", review.__dict__)

    def test_user_id_is_class_attribute(self):
        """Test if 'user_id' is a class attribute of the Review class."""
        review = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(review))
        self.assertNotIn("user_id", review.__dict__)

    def test_text_is_class_attribute(self):
        """Test if 'text' is a class attribute of the Review class."""
        review = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(review))
        self.assertNotIn("text", review.__dict__)

    def test_unique_ids(self):
        """Test that two Review instances have unique IDs."""
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_different_created_at(self):
        """Test that two Review instances have different 'created_at' times."""
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)

    def test_different_updated_at(self):
        """Test that two Review instances have different 'updated_at' times."""
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.updated_at, review2.updated_at)

    def test_str_representation(self):
        """Test the string representation of a Review instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = dt
        review_str = review.__str__()
        self.assertIn("[Review] (123456)", review_str)
        self.assertIn("'id': '123456'", review_str)
        self.assertIn("'created_at': " + dt_repr, review_str)
        self.assertIn("'updated_at': " + dt_repr, review_str)

    def test_instantiation_with_unused_args(self):
        """Test Review instantiation with unused arguments."""
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test Review instantiation with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test Review instantiation with None keyword arguments."""
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

class TestReviewSave(unittest.TestCase):
    """Test cases for the save method of the Review class."""

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
        """Test saving a Review instance once."""
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        self.assertLess(first_updated_at, review.updated_at)

    def test_two_saves(self):
        """Test saving a Review instance twice."""
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        second_updated_at = review.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        review.save()
        self.assertLess(second_updated_at, review.updated_at)

    def test_save_with_arg(self):
        """Test saving a Review instance with an argument (not allowed)."""
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    def test_save_updates_file(self):
        """Test that saving a Review instance updates the file."""
        review = Review()
        review.save()
        review_id = "Review." + review.id
        with open("file.json", "r") as f:
            self.assertIn(review_id, f.read())

class TestReviewToDict(unittest.TestCase):
    """Test cases for the to_dict method of the Review class."""

    def test_to_dict_type(self):
        """Test the data type of the to_dict method's return value."""
        review = Review()
        self.assertTrue(dict, type(review.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test if the to_dict method returns a dictionary with the correct keys."""
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test if to_dict includes added attributes of the Review class."""
        review = Review()
        review.middle_name = "Holberton"
        review.my_number = 98
        self.assertEqual("Holberton", review.middle_name)
        self.assertIn("my_number", review.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test if the datetime attributes in to_dict are strings."""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of the to_dict method."""
        dt = datetime.today()
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that the to_dict method's output is different from __dict__."""
        review = Review()
        self.assertNotEqual(review.to_dict(), review.__dict__)

    def test_to_dict_with_arg(self):
        """Test to_dict with an argument (not allowed)."""
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict(None)

if __name__ == "__main__":
    unittest.main()

