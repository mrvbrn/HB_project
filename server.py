import os
import requests
from flask import Flask, render_template, request, flash, redirect
from model import connect_to_db, Employee, Game, EmployeeGame


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ.get('app.secret_key')

"""API_KEY and password"""

username =os.environ.get('username')
password =os.environ.get('password')




@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/register", methods=['GET'])
def register_form():
    """Show register form for employees signup"""

    return render_template("register_form.html")


@app.route("/register", methods=['POST'])
def register_form():
    """Process registration"""

    employee_id = request.form["employee_id"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]

    new_employee = Employee(employee_id=employee_id, fname=fname, lname=lname, email=email, password=password)

    if Employee.query.get(employee_id):
    	db.session.add(new_employee)
    	db.session.commit
    	flash(f" Employee {email} added.")
    else:
        flash(f" You are not employee.")
        return render_template("/")


@app.route("/top_ten_games")
def top_games():
	"""Show top ten games"""

	return render_template("top_games.html")

@app.route("/kidsappbpox_game")
def kidsappbox_game(game_name):
	"""Show kidsappbox games"""

	return render_template(kidsappbox_game.html)

@app.route("/details_of_games")
def details_of_games(game_name):
	"""Show details of top ten games"""

	return render_template(details_of_games.html)








