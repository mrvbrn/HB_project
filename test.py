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
        """Can teachers see registration form?"""

        result = self.client.get('/register')
        self.assertIn(b"Sign Up", result.data)

    # def test_employee_page(self):
    #     """Can students see registration form?"""

    #     result = self.client.post('/employees/<int:employee_id>')
    #     self.assertIn(b"Welcome", result.data)

    def test_student_log_in_page(self):
        """Can student see log in page?"""

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
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

def test_employee_register(self):
    """can employee register?"""

    employee_info = {'employee_id': "102", 'fname': "Walt", 'lname': "Disney", 'email': "walt@gmail.com", 'password':"password"}
    result = self.client.post("/register", data=employee_info, follow_redirects=True)
    self.assertIn(b"Walt Disney", result.data)


def tearDown(self):
    """Do at end of every test."""

    db.session.close()
    db.drop_all()


if __name__ == "__main__":
    unittest.main()