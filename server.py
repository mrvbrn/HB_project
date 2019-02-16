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


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")



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

# @app.route("/logout")
# dister_foef register_form():
#     """Show register form for employees signup"""

#     return render_template("regrm.html")




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
   

    

    employee_update = Employee.query.filter(Employee.emp_id == emp_id).first()

    if employee_update and employee_update.fname == None:

        employee_update.fname = fname
        employee_update.lname = lname
        employee_update.email = email
        employee_update.password = password

        # new_employee = Employee(emp_id=emp_id, fname=fname, lname=lname, email=email, password=password)
        flash(f" Employee {email} added.")
       
        db.session.commit()

    
    
        # return redirect("/")
    elif employee_update and employee_update.fname != None:
        flash(f" You are  already registered.")
        return redirect("/")

    else:
        flash(f" You are not employee.")
        return redirect("/")

        """Add user information to the session"""
        
    session["fname"] = employee_update.fname
    session["lname"] = employee_update.lname
    session["email"] = employee_update.email



@app.route("/employees")
def employee_list():

    employees = Employee.query.all()

    return render_template("employee.html", employees = employees)

@app.route("/employees/<int:employee_id>")
def user_detail(employee_id):
    """Show info about employee."""

    employee= Employee.query.get(employee_id)
    return render_template("employee.html", employee=employee)

    """Show top twenty games"""





@app.route("/top_twenty_games")
def top_games():

    return render_template("top_games.html")




@app.route("/top_twenty_games", methods = ['POST'])
def top_games_process():
    """Show top twenty games"""

    store = request.form["store"]
    country_code = "US"                    #request.form["country_code"]
    date = request.form["date"]

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
    # import pdb; pdb.set_trace()

    # print (response.json())

    # games = []
   
    # for line in response.iter_lines():
    #     """Load json object and print it out"""
    #     game_dict = json.loads(line)

    #     print(game_dict)
        # games.append(game_dict)


        # print(games)

        # games_list = []

        # for r in json_record:
        #     print (r)



        # print (json_record)

        # responses=response.iter_lines()

        
        # avg_rating = (json_record["avg_rating"]) 
        # rank = (json_record["rank"])
        # app_id = (json_record["app_id"])
        # price = (game_dict["price"])
        # app_name = (json_record["app_name"])
  

    return render_template("top_games.html", json_record=response.iter_lines())
                                             


@app.route("/kidsappbox_game")
def kidsappbox_game(game_name):
	"""Show kidsappbox games"""

	return render_template("kidsappbox_game.html")

       


@app.route("/details_of_games", methods = ['GET', 'POST'])
def details_of_games(app_id):

    """Show details of top ten games"""

    store =request.args["store"]                 # "android"       # Could be either "android" or "itunes".
    country_code = request.args["country_code"]                              #"US"     # Two letter country code.
    app_id = request.args["app_id"]              #"com.facebook.orca" # Unique app identifier (bundle ID).

    req_params = {"country": country_code}

    # Request URL
    url = "https://api.appmonsta.com/v1/stores/%s/details/%s.json" % (store, app_id)

    # This header turns on compression to reduce the bandwidth usage and transfer time.
    headers = {'Accept-Encoding': 'deflate, gzip'}

    # Python Main Code Sample
    response = requests.get(url,
                            auth=(username, password),
                            params=req_params,
                            headers=headers,
                            stream=True)

    print (response.status_code)
    for line in response.iter_lines():
    # Load json object and print it out
       json_record = json.loads(line)
       print (json_record)
    return render_template("details_of_games.html", description=description)

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")

              
              
              
              
              
              
              
              
              
              
              
