import unittest
from unittest import TestCase
import controller_admin

class Testcontroller_admin(unittest.TestCase):

    def setUp(self):
        # This method is called before each test
        self.admin_controller = controller_admin.controller_admin()
        # Set up any necessary initial data or configurations here

    def test_read_admin(self):
        # Expected data to match against
        expected_admin_data = {
            'Username': "admin",
            'Password': "parrucca",
            # Add other expected fields
        }

        # Call the method to test
        admin_data = self.admin_controller.read_admin("admin")

        # Perform assertions to check if the output is as expected
        self.assertEqual(admin_data['Username'], expected_admin_data['Username'])
        self.assertEqual(admin_data['Password'], expected_admin_data['Password'])
        # Add more assertions as necessary to validate all important fields

        # Optionally, check for types, not just values
        self.assertIsInstance(admin_data, dict)
        self.assertIsInstance(admin_data['Username'], str)
        self.assertIsInstance(admin_data['Password'], str)
        # Add more type checks as necessary

if __name__ == '__main__':
    unittest.main()