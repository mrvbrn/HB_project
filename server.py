import os
import requests
import json
from flask import Flask, render_template, request, flash, redirect, session
from model import connect_to_db, db, Employee, Game, EmployeeGame
from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = 'ABC'

"""API_KEY and password"""

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')




@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")



@app.route("/", methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    employee = Employee.query.filter_by(email=email).first()



    if not employee:
        flash("No such employee")
        return redirect("/register")

    if employee.password != password:
        flash("Incorrect password")
        return redirect("/")

    session["employee_id"] = employee.employee_id

    flash("You are successfully log in")
    return redirect(f"/employees/{employee.employee_id}")


@app.route("/register", methods=['GET'])
def register_form():
    """Show register form for employees signup"""

    return render_template("register_form.html")


@app.route("/register", methods=['POST'])
def register_process():
    """Process registration"""

    emp_id = request.form["emp_id"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]

    

    if Employee.query.filter(Employee.emp_id == emp_id).first():

        new_employee = Employee(emp_id=emp_id, fname=fname, lname=lname, email=email, password=password)
        flash(f" Employee {email} added.")
        db.session.add(new_employee)
    
    
        return redirect("/")
    else:
        flash(f" You are not employee.")
        return redirect("/")
    db.session.commit()

# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""

#     return render_template("login_form.html")

# @app.route("/employee/<employee_id>")
# def employee_detail(employee_id):
#     """Show info about user."""

#     user = Employee.query.get(employee_id)
#     return render_template("employee.html", employee=employee)




@app.route("/top_twenty_games")
def top_games():
    """Show top twenty games"""

store = "android"        #register_form["store"]
country_code = "US"           #register_form["country_code"]
date = "2019-02-12"                   #register_form["date"]

req_params = {"date" : date,
                  "country" : country_code}

request_url = request_url = "https://api.appmonsta.com/v1/stores/%s/rankings.json" % store
headers = {'Accept-Encoding': 'deflate, gzip'}

# Python Main Code Sample
response = requests.get(request_url,
                        auth=(username, password),
                        params=req_params,
                        headers=headers,
                        stream=True)

print (response.status_code)
for line in response.iter_lines():
  # Load json object and print it out
  json_record = json.loads(line)
  print (json_record)
	# return render_template("top_games.html")

@app.route("/kidsappbpox_game")
def kidsappbox_game(game_name):
	"""Show kidsappbox games"""

	return render_template(kidsappbox_game.html)

@app.route("/details_of_games")
def details_of_games(game_name):
	"""Show details of top ten games"""

	return render_template(details_of_games.html)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")

              
              
              
              
              
              
              
              
              
              
              
