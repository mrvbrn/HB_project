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
                       primary_key=True)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

   
  

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Employee employee_id={self.employee_id} fname={self.fname} lname={self.lname} email={self.email}>"
 

class Game(db.Model):
    """Games of KidsAppBox; stored in a database"""

    __tablename__ = "games"

    game_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    game_name = db.Column(db.String(100))
    app_id = db.Column(db.String(100))
    store = db.Column(db.String(20))
    image=db.Column(db.String(50))

  
    employees = db.relationship("Employee", secondary = "employee_games", backref = "games")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Game game_id={self.game_id} gname={self.game_name} app_id={self.app_id} store={self.store} image={self.image}>"

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

def example_data():
    """sample data for testing"""

    #In case this is run more than once, empty out existing data

    Employee.query.delete()
    Game.query.delete()
    EmployeeGame.query.delete()

    # add sample employees, games and employeegames

    leonard = Employee(employee_id="111", fname='Leonard', lname='Asby', email='leonard@gmail.com', password='test')
    liz = Employee(employee_games="108", fname='Liz', lname='Asby', email='liz@gmail.com', password='test')
    meggie = Employee(employee_games="104", fname='Meggie', lname='Asby', email='meggie@gmail.com', password='test')

    game1 = Game(game_name = 'First Words for Baby', app_id = 'com.androbaby.firstwordsforbaby', store = "android", image = "/static/image/first_words.jpg")
    game2 = Game(game_name = 'Kids Construction Game: Preschool', app_id = 'com.androbaby.kidsconstructiongame', store = "android", image = "/static/image/kids_construction.jpg")
    game3 = Game(game_name = 'Kids Jigsaw Puzzles: Farm', app_id = '1272837891', store = "android", image = "/static/image/kids_farm.jpg")

    employeegame1 = EmployeeGame(employee_id="111", game_id="1")
    employeegame2 = EmployeeGame(employee_id="108", game_id="2")
    employeegame3 = EmployeeGame(employee_id="103", game_id="29")

    db.session.add_all(leonard, liz, meggie, game1, game2, game3, employeegame1, employeegame2, employeegame3)
    db.session.commit()
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
   