import os
import pprint
import requests
import json
import time
from flask import Flask, render_template, request, flash, redirect, session, jsonify
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
     
    return render_template("login.html")



@app.route("/login.json", methods=['POST'])
def login_process():

    email = request.form["email_info"]
    password = request.form["password_info"]
    employee = Employee.query.filter_by(email=email).first()
  

    if not employee:

        data = {

        'email' : email,
        'password' : password,
        'employee' : None,
        }

    else:
        confirm_password = employee.password
        confirm_email = employee.email
        employee_ids = employee.employee_id


        data = {

        'email' : email,
        'password' : password,
        'employee_ids' : employee_ids,
        'employee' : confirm_email,
        'confirm_password' : confirm_password,
        'confirm_email' : employee.email,
        }

   

    return jsonify(data)


@app.route('/login_employee/<int:employee_id>')
def login_employee(employee_id):

    session["employee_id"] = employee_id 

    return redirect(f'/employees/{employee_id}')
   


@app.route('/logout')
def logout():
    """Log out."""
    
    del session["employee_id"]
    flash("You are succesfully log out.")
    return redirect("/")


@app.route("/register", methods=['GET'])
def register_form():
    """Show register form for employees signup"""

    return render_template("register_form.html")


@app.route("/register", methods=['POST'])
def register_process():
    """Process registration"""

    employee_id = request.form["employee_id"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]


   

    

    employee_update = Employee.query.filter(Employee.employee_id == employee_id).first()


    if password == confirm_password:

        if employee_update and employee_update.fname == "null":

            """add the employee to the database"""

            employee_update.fname = fname
            employee_update.lname = lname
            employee_update.email = email
            employee_update.password = password
            """create new employee"""

            new_employee = Employee(employee_id= employee_id, fname=fname, lname=lname, email=email, password=password)
            flash(f" Employee {fname} {lname} added.")
            db.session.add(new_employee)
            db.session.commit()



            return redirect("/login")
        elif employee_update and employee_update.fname != None:
            flash(f" You are  already registered.")
            return redirect("/login")

        else:
            flash(f" You are not employee.")
            return redirect("/")
    
    else:

        flash(f" Password does not match.")
        return redirect("/register")


        """Add employee information to the session"""
        
    session["fname"] = employee_update.fname
    session["lname"] = employee_update.lname
    session["email"] = employee_update.email


@app.route("/employees/<int:employee_id>")
def employee_detail(employee_id):

    """Show info about employee."""
   
    employee= Employee.query.get(employee_id)
  
    return render_template("employee.html", employee=employee)


@app.route("/top_twenty_games")
def top_games():

    return render_template("top_games.html")


@app.route("/top_twenty_games", methods=['POST'])
def top_games_process():
    """Show top twenty games"""

    store = request.form["store_type"]
    country_code = request.form["country_type"]
    date = request.form["date_type"]

    req_params = {"date" : date,
                  "country" : country_code}

    request_url = request_url = f"https://api.appmonsta.com/v1/stores/{store}/rankings.json" 
    headers = {'Accept-Encoding': 'deflate, gzip'}

    # Python Main Code Sample
    response = requests.get(request_url,
                            auth=(username, password),
                            params=req_params,
                            headers=headers,
                            stream=True)

    games = []
    games_seen = set()
    for line in response.iter_lines():
       
        """  if api don't give data for selected time and country display no data""" 

        game_dict = json.loads(line)
        if game_dict:
            try:
                if game_dict['app_id'] not in games_seen:
                    games.append(game_dict)                      # remove repetetion     
                    games_seen.add(game_dict['app_id'])
                    game = sorted(games, key=lambda i: i['rank'])[:20]   # sorted by rank
                
           
            except KeyError:
                game = 'No Data'
           

    return render_template("top_games.html", json_record=game, store=store, country=country_code)          


@app.route("/employees/<int:employee_id>/kidsappbox_game", methods=['GET'])
def kidsappbox_game(employee_id):

    """select employee's game"""
    games = db.session.query(Game).join(EmployeeGame).filter(EmployeeGame.employee_id == employee_id).all()
    employee = Employee.query.get(employee_id)
    """ make a list of employeeis game"""
    game_list=[]
    id_list=[] 
    

    for game in games:
        if [game.game_name, game.image] not in game_list:

            game_list.append([game.game_name, game.image])

           
    app_id = game.app_id
   

    return render_template("kidsappbox.html", games=games, employee=employee, app_id=app_id)
  


@app.route("/game-data/<int:game_id>")
def kidsappbox_process(game_id):

    country = "US"
    
    game = Game.query.get(game_id)
    store = game.store

    # games = db.session.query(Game).join(EmployeeGame).filter(EmployeeGame.employee_id == employee_id).filter(Game.store == store).filter(Game.game_name == gamename).all()
    req_params = {"country": country}
    
    # Request URL
    url = f"https://api.appmonsta.com/v1/stores/{store}/details/{game.app_id}.json" 
    # 'all_histogram': {'1': 15, '3': 2, '2': 4, '5': 20, '4': 8}
    # This header turns on compression to reduce the bandwidth usage and transfer time.
    headers = {'Accept-Encoding': 'deflate, gzip'}

    # Python Main Code Sample
    response = requests.get(url,
                            auth=(username, password),
                            params=req_params,
                            headers=headers,
                            stream=True)
    """ details of single app"""
    game_data = response.json()

    """sort dict by the key"""

    sorted_dict = dict(sorted((game_data.get('all_histogram')).items()))
   
    if sorted_dict:

        data_dict = {
                    "labels": list(sorted_dict.keys()),
                    "datasets": [
                        {
                            "data": list(sorted_dict.values()),
                            "backgroundColor": [
                                "#FF6384",
                                "#36A2EB",
                                "#FFCE56",
                                "purple",
                                "yellow"
                            ],
                            "hoverBackgroundColor": [
                                "#FF6384",
                                "#36A2EB",
                                "#FFCE56",
                                "purple",
                                "yellow"
                            ]
                        }]
                }
        return jsonify(data_dict)

    else:
        return jsonify('No data for this game')
  
             

@app.route("/details_of_games/<string:country>/<string:store>/<string:app_id>", methods = ['GET', 'POST'])
def details_of_games(country, store, app_id):

    """Show details of top twenty games"""
    req_params = {"country": country}

    # Request URL
    url = f"https://api.appmonsta.com/v1/stores/{store}/details/{app_id}.json"

    # This header turns on compression to reduce the bandwidth usage and transfer time.
    headers = {'Accept-Encoding': 'deflate, gzip'}

    # Python Main Code Sample
    response = requests.get(url,
                            auth=(username, password),
                            params=req_params,
                            headers=headers,
                            stream=True)

    games=[]


    for line in response.iter_lines():
    # Load json object and print it out
       json_record = json.loads(line)
       games.append(json_record)
    return render_template("details_of_games.html", json_record=games)


@app.route("/details_any_games", methods=['GET'])
def details_any_games():
    """Show the form"""

    return render_template("details_any_games.html")
  


@app.route("/details_any_games", methods=['POST'])
def show_details():

    country = request.form["country_type"]
    store = request.form["store_type"]
    app_id = request.form["app_id_type"]

    req_params = {"country": country}

    # Request URL
    url = f"https://api.appmonsta.com/v1/stores/{store}/details/{app_id}.json" 

    # This header turns on compression to reduce the bandwidth usage and transfer time.
    headers = {'Accept-Encoding': 'deflate, gzip'}

    # Python Main Code Sample
    response = requests.get(url,
                            auth=(username, password),
                            params=req_params,
                            headers=headers,
                            stream=True)

   
    for line in response.iter_lines():
    # Load json object and print it out
       single_app_record = json.loads(line)
    
    return jsonify(single_app_record)



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")

              
              
              
              
              
              
              
              
              
              
              
