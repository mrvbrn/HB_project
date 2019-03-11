import unittest 
from server import app
from model import connect_to_db, db, example_data
from flask import session
class FlaskTestsBasic(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"KidsAppBox", result.data)


    def test_register_page(self):
        """Test register page"""

        result = self.client.get('/register')
        self.assertIn(b"Sign Up", result.data)

    def login_page(self):
      

        result = self.client.get('/login')

        self.assertIn(b"Email Adress", result.data)

    def test_top_games_page(self):
        """Test top twenty game"""

        result = self.client.get('/top_twenty_games')
        self.assertIn(b"top twenty games", result.data)

    def test_details_of_games_page(self):
        """Test details of games page"""

        result = self.client.get('/top_twenty_games')
        self.assertIn(b"top twenty games", result.data)


 

class EmployeeTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_employee_register(self):
        """can employee register?"""

        employee_info = {'employee_id': "111", 'fname': "Leonard", 'lname': "Asby", 'email': "leonard@gmail.com", 'password':"test", "confirm_password": "test"}
        result = self.client.post("/register", data=employee_info, follow_redirects=True)
        self.assertIn(b"already registered", result.data)





if __name__ == "__main__":
    unittest.main()