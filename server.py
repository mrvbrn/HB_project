import os
import pprint
import requests
import json
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
      # Get form variables
    


    return render_template("login.html")



@app.route("/login.json", methods=['POST'])
def login_process():

    email = request.form["email_info"]
    password = request.form["password_info"]
    employee = Employee.query.filter_by(email=email).first()
    # confirm_password = employee.password
    # confirm_email = employee.email
  

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



# @app.route("/login", methods=['POST'])
# def login_process():
#     """Process login."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]
#     employee = Employee.query.filter_by(email=email).first()



#     if not employee:
#         flash("No such employee")
#         return redirect("/register")

#     if employee.password != password:
#         print(employee.password)
#         print(password)
#         flash("Incorrect password")
#         return redirect("/login")

#     session["employee_id"] = employee.employee_id

#     flash("You are successfully log in")
#     return redirect(f"/employees/{employee.employee_id}")


@app.route("/logout")
def log_out():
    """log out of employee's account"""

    session.clear()

    return render_template("log_out.html")




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

            flash(f" Employee {email} added.")
           
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

    store = request.form["store"]
    country_code = request.form["country"]
    date = request.form["date"]

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
        """Load json object and print it out"""

        game_dict = json.loads(line)
        if game_dict['app_id'] not in games_seen:
            games.append(game_dict)
            games_seen.add(game_dict['app_id'])

    game = sorted(games, key=lambda i: i['rank'])[:20]
    




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
           

   

    return render_template("kidsappbox.html", games=games, employee=employee)





@app.route("/game-data/<int:game_id>")
def kidsappbox_process(game_id):

    # store = request.form["store_type"]
    # country_code = request.form["country_type"]
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

    game_data = response.json()

    print(game_data.get('all_histogram'))
    if game_data.get('all_histogram'):

        data_dict = {
                    "labels": list(game_data['all_histogram'].keys()),
                    "datasets": [
                        {
                            "data": list(game_data['all_histogram'].values()),
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

    # print (response.status_code)

    games=[]


    for line in response.iter_lines():
    # Load json object and print it out
       json_record = json.loads(line)
       print(json_record)
       games.append(json_record)
    return render_template("details_of_games.html", json_record=games)


@app.route("/details_any_games", methods=['GET'])
def details_any_games():
    """Show the form"""

    return render_template("details_any_games.html")



@app.route("/details_any_games", methods=['POST'])
def show_details():
    #import pdb; pdb.set_trace()
    """select country, store and App_id"""
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
       json_record = json.loads(line)
    
    return jsonify(json_record)



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")

              
              
              
              
              
              
              
              
              
              
              
