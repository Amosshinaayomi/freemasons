from flask import Flask, redirect, render_template, request, session, send_file
from flask_session import Session
from cs50 import SQL 
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology
import os
import requests 
import json
from flask import jsonify
import requests.exceptions
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from helpers import get_services
import random
app = Flask(__name__)
geolocator = Nominatim(user_agent="freemasons", timeout=10)



app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")
uploads_dir = "uploads"
uploads_dir = os.path.join("static", uploads_dir)
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    fullname = db.execute("SELECT firstname, lastname FROM users WHERE id=?", session['user_id'])
    if not fullname:
        return redirect("/register")
    fullname = fullname[0]
    response = requests.get('https://nigeria-states-towns-lga.onrender.com/api/states')         
    states = response.json()
    services = db.execute("SELECT service_name FROM services")
    if not services:
        services = get_services()
        for service in services:
            try:
                db.execute("INSERT INTO services (service_name) VALUES (?)", service)

            except:
                break
        services = db.execute("SELECT service_name FROM services")   
    return render_template("index.html", firstname=fullname['firstname'], lastname=fullname['lastname'], states=states, services=services)

def get_location_by_name(name):
    """Get latitude and longitude by location name using geopy."""
    try:
        location = geolocator.geocode(name)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        print(f"Error: geocode failed on input {name} with message timed out")
        return None, None

@app.route('/load-town-city', methods=['GET'])
@login_required 
def load_towns_cities_lgas():
    state_name = request.args.get('state')
    state_name = state_name.upper()
    print(f"state name is {state_name}")    

    try:
        # Fetch towns and cities
        response_towns = requests.get(f'https://nigeria-states-towns-lga.onrender.com/api/{state_name}/towns')
        response_towns.raise_for_status()

        # Fetch LGAs
        # response_lgas = requests.get(f'https://nigeria-states-towns-lga.onrender.com/api/{state_name}/lgas')
        # response_lgas.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return jsonify({"message": "Unable to fetch data from the server"}), 500
    except Exception as err:
        print(f"An error occurred: {err}")
        return jsonify({"message": "Something went wrong"}), 500
    else:
        towns_cities = response_towns.json()
        # lgas = response_lgas.json()

        # towns_cities.extend(lgas)  # Append LGAs to the towns and cities list
        return jsonify({'towns_cities': towns_cities})

@app.route('/get-location', methods=['GET'])
@login_required 
def get_location():
    state_name = request.args.get('state')
    town_city_name = request.args.get('town_city')
    lat, lon = get_location_by_name(f"{town_city_name}, {state_name}, Nigeria")
    if lat and lon:
        location = {"latitude": lat, "longitude": lon}
    else:
        location = None
    print(f'location is {jsonify(location)}')
    return jsonify(location)


@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    firstname = firstname.strip()
    lastname = lastname.strip()

    password = request.form.get("password")
    if not firstname:
        return apology("full-name wasn't provided", " to go back to login page", "/login")

    if not lastname:
        return apology("full-name wasn't provided", " to go back to login page", "/login")  

    if not password:
        return apology("password wasn't provided", " to go back to login page", "/login")


    row = db.execute("SELECT * FROM users WHERE firstname=? AND lastname=?", firstname, lastname)
    print(f'row is {row}')   

    if not row:
        return apology("invalid fullname and/ or password", " to go back to login page", "/login")



    if len(row) >= 1:
        for i in range(len(row)):
            if check_password_hash(row[i]['hash'], password):
                session['user_id'] = row[0]['id']
                return redirect("/")

    return apology("invalid fullname and/ or password", " to go back to login page", "/login")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    gender = request.form.get("gender")
    password = request.form.get("password")
    confirmed_password = request.form.get("confirm_password")

    if not firstname:
        return apology("firstname not provided", " to go back to registration page", "/register")
    
    if not lastname:
        return apology("lastname not provided", " to go back to registration page", "/register")

    if not gender:
        return apology("please choose your gender", " to go back to registration page", "/register")

    if not password:
        return apology("password not provided", " to go back to registration page", "/register")
    

    if not confirmed_password:
        return apology("confirm your password", " to go back to registration page", "/register")
    
    if password != confirmed_password:
        return apology("passwords do not match", " to go back to registration page", "/register")
    
    hash_password = generate_password_hash(password)
    confirm_hash = db.execute("SELECT id FROM users WHERE hash=?", hash_password)

    if confirm_hash:
        return apology("sorry, password has already been taken", " to go back to registration page", "/register")
    
    firstname = firstname.strip()
    lastname = lastname.strip()

    db.execute("INSERT INTO users(firstname, lastname, hash, gender) VALUES(?, ?, ?, ?)", firstname, lastname, hash_password, gender)

    return redirect("/login")
    


@app.route("/logout")
def logout():
    """log user out"""
    session.clear()
    return redirect("/")


@app.route("/update_profile", methods=['GET', 'POST'])
@login_required
def update_profile():
    fullname = db.execute("SELECT firstname, lastname FROM users WHERE id=?", session['user_id'])
    if not fullname:
        return redirect("/register")
    if request.method == 'GET':
        response = requests.get('https://nigeria-states-towns-lga.onrender.com/api/states')         
        states = response.json()
        services = db.execute("SELECT service_name FROM services")
        print(f'services are {services}')
        if not services:
            services = get_services()
            for service in services:
                try:
                    db.execute("INSERT INTO services (service_name) VALUES (?)", service)

                except:
                    break
        services = db.execute("SELECT service_name FROM services")   
        print(f'service is {services}')   
        return render_template("update_profile.html", states=states, services=services)

    phone_number = request.form.get("phone_number")
    image = request.files["image"]
    email = request.form.get("email")
    state = request.form.get("state")
    area = request.form.get('area')
    service = request.form.get('service')
    service_id = db.execute('SELECT id FROM services WHERE service_name=?', service)
    if not service_id:
        return apology("no service id", " to go back to profile page", "/profile")
    

    service_id = service_id[0]['id']
    # print(f'service id is {service_id}')
    if not email or not phone_number  or not state or not area or not service:
        return apology("full details not provided", )
    
    email = email.strip()
    phone_number = phone_number.strip()
    state = state.strip()
    area = area.strip()
    service = service.strip()

    filename = image.filename
    try:
        unique_image_path = f"{os.urandom(16).hex()}.{filename.rsplit('.', 1)[1]}"

        image.save(os.path.join(uploads_dir, unique_image_path))
        db.execute("INSERT INTO images (image_path, person_id) VALUES(?, ?)", unique_image_path, session["user_id"])
        db.execute('INSERT INTO masons (person_id, service_id, town, state, email, phone_number) VALUES (?,?,?,?,?,?)', session['user_id'], service_id, area, state, email, phone_number)
        
        print("info successfully stored in database")        
        print("done here")
    except Exception:
        return apology("couldn't update details", " to go back to profile page", "/profile")

    return redirect("/profile")

@app.route("/profile")
@login_required
def profile():
        fullname = db.execute("SELECT firstname, lastname FROM users WHERE id=?", session['user_id'])
        if not fullname:
            return redirect("/register")
        fullname = fullname[0]
        if request.method == "GET":
            # get user image from db
            user_image = db.execute("SELECT image_path FROM images WHERE person_id=?", session['user_id'])
            
            phone_number = db.execute("SELECT phone_number FROM masons WHERE person_id=?", session['user_id'])

            state = db.execute("SELECT state FROM masons WHERE person_id=?", session['user_id'])

            city = db.execute("SELECT town FROM masons WHERE person_id=?", session['user_id'])



            email = db.execute("SELECT email FROM masons WHERE person_id=?", session['user_id'])

            service_id = db.execute("SELECT service_id FROM masons WHERE person_id=?", session['user_id'])

   

            if not phone_number or not email or not state:
                return redirect("/update_profile")
            service_id = service_id[0]['service_id']
            service_name = db.execute("SELECT service_name FROM services WHERE id=?", service_id) 

            user_image = user_image[0]['image_path']
            user_image = os.path.join(uploads_dir, user_image)
            service_name = service_name[0]['service_name']
            phone_number = phone_number[0]['phone_number']
            state = state[0]['state']
            city = city[0]['town']
            email = email[0]['email']

            response = requests.get('https://nigeria-states-towns-lga.onrender.com/api/states')         
            states = response.json()
            return render_template("profile.html", image_path=user_image, states=states, email=email, city=city, phone_number=phone_number, service=service_name, fullname=fullname, state=state, user_state=state, user_city=city)
        
@app.route("/edit_info", methods=["POST"])
@login_required
def edit():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    mobile_number = request.form.get("mobilenumber")
    email = request.form.get("state")
    area = request.form.get("area")

    if not firstname or not lastname or not mobile_number or not email or not area:
        return apology("no info was provided", "go click here to go back to profile page", "/profile")
    
    db.execute("")


@app.route("/get-people")
@login_required
def get_people():
    state = request.args.get('state')
    town_city = request.args.get('town_city')

    people = db.execute("SELECT users.firstname, users.lastname, masons.phone_number, masons.email, services.service_name FROM masons JOIN users ON masons.person_id = users.id JOIN services ON masons.service_id = services.id WHERE masons.state = ? AND masons.town = ?", state, town_city)

    latitude, longitude = get_location_by_name(f"{town_city}, {state}")

    # Add the location data to the people data
    for person in people:
        offset = lambda: random.uniform(-0.0065, 0.0065)
        person['latitude'] = latitude + offset()
        person['longitude'] = longitude + offset()

    return jsonify(people)


@app.route('/edit', methods=['POST'])
def edit_profile():
    # Get form data
    firstname = request.form.get('firstname')
    
    lastname = request.form.get('lastname')
    mobilenumber = request.form.get('mobilenumber')
    email = request.form.get('email')
    state = request.form.get('state')
    area = request.form.get('area')

    # Check if at least one field is filled
    if firstname or lastname or mobilenumber or email or state or area:
        # Update the database
    # Update the database only if a field is provided
        if firstname:
            firstname = firstname.strip()
            db.execute("UPDATE users SET firstname = ? WHERE id = ?", firstname, session['user_id'])
        if lastname:
            lastname = lastname.strip()
            db.execute("UPDATE users SET lastname = ? WHERE id = ?", lastname, session['user_id'])
        if mobilenumber:
            mobilenumber= mobilenumber.strip()
            db.execute("UPDATE masons SET phone_number = ? WHERE person_id = ?", mobilenumber, session['user_id'])
        if email:
            email = email.strip()
            db.execute("UPDATE masons SET email = ? WHERE person_id = ?", email, session['user_id'])
        if state:
            db.execute("UPDATE masons SET state = ? WHERE person_id = ?", state, session['user_id'])
        if area:

            db.execute("UPDATE masons SET town = ? WHERE person_id = ?", area, session['user_id'])
    else:
        return apology("Please provide at least one info to edit", "go back to profile page", "/profile")

    return redirect("/profile")
