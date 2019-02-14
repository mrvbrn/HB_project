"""Models and database functions for KidsAppBox's employee"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class Employee(db.Model):
    """Employees of KidsAppBox; stored in a database"""

    __tablename__ = "employees"

    employee_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    emp_id = db.Column(db.Integer, nullable=False, unique=True)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

   
  

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Employee user_id={self.employee_id} fname={self.fname} lname={self.lname} email={self.email}>"
 

class Game(db.Model):
    """Games of KidsAppBox; stored in a database"""

    __tablename__ = "games"

    game_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    game_name = db.Column(db.String(100))
    game_description = db.Column(db.Text)

  
    employees = db.relationship("Employee", secondary = "employee_games", backref = "games")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Game user_id={self.game_id} fname={self.game_name} lname={self.game_description}>"

class EmployeeGame(db.Model):
    """ Association table between Employee and Game"""

    __tablename__ = "employee_games"



    employee_game_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    employee_id = db.Column(db.Integer, 
    	                    db.ForeignKey("employees.employee_id"),
    	                    nullable = False)
    game_id = db.Column(db.Integer, 
                        db.ForeignKey("games.game_id"),
    	                nullable = False)




    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<EmployeeGame employee_game_id={self.employee_game_id} employee_id={self.employee_id} game_id={self.game_id}>"

       


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///employees'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")




   