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

    return render_template("login.html")



@app.route("/login", methods=['POST'])
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
        return redirect("/login")

    session["employee_id"] = employee.employee_id

    flash("You are successfully log in")
    return redirect(f"/employees/{employee.employee_id}")

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
    

    game_list=[]
    img_list=[]

    for game in games:
        if game.game_name not in game_list and game.image not in img_list:
            game_list.append(game.game_name)
            img_list.append(game.image)

    

    return render_template("kidsappbox.html", games=game_list, images=img_list)





@app.route("/employees/<int:employee_id>/kidsappbox_game", methods=['POST'])
def kidsappbox_process(employee_id):

    """select employee's game"""
    games = db.session.query(Game).join(EmployeeGame).filter(EmployeeGame.employee_id == employee_id).all()
	
    for game in games:
        app_id = game.app_id
        store = "android"
        print(app_id)
    
    # country = "US"
  

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

    print (response.status_code)

   
    for line in response.iter_lines():
    # Load json object and print it out
       json_record = json.loads(line)
    
 

      
    return render_template("kidsappbox.html", json_record=json_record)


@app.route("/kidsappbox_game", methods=['POST'])
def kidsappbox_game_process(game_name):
    """Show kidsappbox game information"""

    return render_template("kidsappbox_game.html")

       


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

    # print (response.status_code)

   
    for line in response.iter_lines():
    # Load json object and print it out
       json_record = json.loads(line)
    
    return jsonify(json_record)

# @app.route("/top_twenty_games.json")
# def top_games_json():






if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")

              
              
              
              
              
              
              
              
              
              
              
