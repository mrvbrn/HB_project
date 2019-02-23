
from sqlalchemy import func

from model import Employee, Game, EmployeeGame, connect_to_db, db
from server import app

def load_employees(employee_filename):
    """Load games from game.data into database."""

    print("Employees")

    for i, row in enumerate(open(employee_filename)):
        row = row.rstrip()
        employee_id, fname, lname, email = row.split("|")[:4]
        print(row.split("|")[:4])

        employee = Employee(employee_id=employee_id,
        	        fname=fname,
                    lname=lname,
                    email=email)

        # We need to add to the session or it won't ever be stored
        db.session.add(employee)

        # provide some sense of progress
        if i % 10 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()
def load_games(game_filename):
    """Load games from game.data into database."""

    print("Games")

    for i, row in enumerate(open(game_filename)):
        row = row.rstrip()
        game_id, store, app_id, game_name, image= row.split("|")

        game = Game(game_id=game_id,
        	        store=store,
        	        app_id=app_id,
                    game_name=game_name,
                    image=image)

        # We need to add to the session or it won't ever be stored
        db.session.add(game)

        # provide some sense of progress
        if i % 10 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()


def load_employee_games(employee_game_filename):
    """Load association table from employee_game into database."""

    print("Employee_games")

    for i, row in enumerate(open(employee_game_filename)):
        row = row.rstrip()
        employee_game_id, employee_id, game_id = row.split("|")[:3]



        employee_game_id=int(employee_game_id)
        game_id=int(game_id)
        employee_id=int(employee_id)

        employee_game = EmployeeGame(employee_game_id=employee_game_id,
                                    game_id=game_id,
                                    employee_id=employee_id)

   
        db.session.add(employee_game)

        # provide some sense of progress
        if i % 10 == 0:
            print(i)


    # Once we're done, we should commit our work
    db.session.commit()


def set_val_emp_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Employee.employee_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('employees_employee_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    employee_filename = "seed_data/employee.data"
    game_filename = "seed_data/game.data"
    employee_game_filename="seed_data/employee-game.data"
    load_employees(employee_filename)
    load_games(game_filename)
    load_employee_games(employee_game_filename)
    set_val_emp_id()



