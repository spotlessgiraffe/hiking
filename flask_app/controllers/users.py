from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.hike import Hike
from flask_bcrypt import Bcrypt     # so that we can hash our passwords later

# We are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument
bcrypt = Bcrypt(app)

# -- Landing page --
@app.route("/")
def index():
    return render_template("index.html")

# -- Register page --
@app.route("/register")
def register():
    return render_template("register.html")

# -- Process user input entered on register form --
@app.route ("/create/user", methods=["POST"])
def register_user():
    if not User.validate_reg(request.form):
        return redirect("/register")
    
    # If registration inputs are valid:
    # Hash the password before saving into database
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }

    # Save all user input into database and grab the row id we just filled in
    user_id = User.save(data)
    # Store user in session by storing the returned user id so that we can query for user info in database just by calling on the id
    session["user_id"] = user_id
    # Redirect to success page
    return redirect("/dashboard")

# -- Process user input on login form --
@app.route("/login", methods=["POST"])
def login():
    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }

    # -- Validate the user input on the login form --
    # See if we can find a user with the same email input
    user_db = User.get_by_email(data)
    # If we cannot find a match, flash an error message
    if not user_db:
        flash("Invalid email/password!", "login")
        return redirect("/")
    # If email exists in the database and if entered password does not match corresponding hash in database
    if not bcrypt.check_password_hash(user_db.password, request.form["password"]):
        flash("Invalid email/password!", "login")
        return redirect("/")
    
    # Otherwise, if login is valid, store the user in session and then redirect to the dashboard 
    session["user_id"] = user_db.id
    return redirect("/dashboard")

# -- Dashboard page -- 
@app.route("/dashboard", methods=["GET", "POST"])
def welcome():
    if "user_id" not in session:
        return redirect("/logout")

    user_data = {
        "id": session["user_id"]
    }

    hikes_with_users = []   # This will be a list of Hike objects
    hike_id_index = 1

    if request.method == "POST":
        if (request.form["state"] != "no_filter") or (request.form["city"] != "no_filter") or (request.form["difficulty"] != "no_filter"):
            if request.form["state"] != "no_filter":
                data = {
                    "state": request.form["state"]
                }
                filtered_hikes = Hike.sort_by_filter(data)
            elif request.form["city"] != "no_filter":
                data = {
                    "city": request.form["city"]
                }
                filtered_hikes = Hike.sort_by_filter(data)
            else:
                data = {
                    "difficulty": request.form["difficulty"]
                }
                filtered_hikes = Hike.sort_by_filter(data)

            # filtered_hikes = Hike.sort_by_filter(data)
            print(filtered_hikes)

            while hike_id_index <= len(filtered_hikes):
                hike_data = {
                    "id": hike_id_index
                }

                hikes_with_users.append(Hike.get_with_user(hike_data))      # Populate hikes_with_users with specified hike data
                hike_id_index += 1
            
            print(filtered_hikes)
            return render_template("dashboard.html", current_user = User.get_by_id(user_data), hikes_with_users = hikes_with_users)
    else: 
        # List of hikes
        all_hikes = Hike.get_all()  # Check if there are any hike posts first

        for hike in all_hikes:
            latest_hike = Hike.get_latest()
            if hike.id <= latest_hike.id:
                hike_data = {
                    "id": hike.id
                }

                hike_with_user = Hike.get_with_user(hike_data)
                hikes_with_users.append(hike_with_user)

    return render_template("dashboard.html", current_user = User.get_by_id(user_data), hikes_with_users = hikes_with_users)

# -- View profile of logged-in user --
@app.route("/profile")
def user_profile():
    if "user_id" not in session:
        return redirect("/logout")
    
    data = {
        "id": session["user_id"]
    }

    # List of hikes
    fave_hikes_with_users = []   # This will be a list of Hike objects
    all_hikes = Hike.get_all()  # Check if there are any hike posts first
    
    current_user = User.get_user_faves(data)    # Will allow us to access the user's list of fave hikes

    if len(all_hikes) != 0:  # If there are hike posts, grab the latest post
        latest_hike = Hike.get_latest()

        hike_id_index = 1
        while hike_id_index <= latest_hike.id:
            hike_data = {
                "id": hike_id_index
            }

            # Check if the current hike is on user's favorites list
            for fave_hike in current_user.with_faves:
                if hike_id_index == fave_hike.id:
                    fave_hikes_with_users.append(Hike.get_with_user(hike_data))
                
            hike_id_index += 1

    return render_template("profile.html", user = User.get_by_id(data), fave_hikes_with_users = fave_hikes_with_users)

# -- Form to edit profile --
@app.route("/profile/edit")
def edit_profile():
    if "user_id" not in session:
        return redirect("/logout")
    
    data = {
        "id": session["user_id"]
    }
    return render_template("edit_profile.html", user = User.get_by_id(data))

# -- Process user input on form to update user's profile --
@app.route("/profile/update", methods=["POST"])
def update_profile():
    # Validate "Edit Profile" user inputs
    if not User.validate_profile(request.form):
        return redirect("/profile/edit")
    
    if request.form["password"] != "":   # If user entered a new password (value of "" indicates user did not enter a new password)
        data = {
            "id": session["user_id"],
            "about_me": request.form["about_me"],
            "experience_level": request.form["experience"],
            "password": bcrypt.generate_password_hash(request.form["password"])
        }
        
        User.update_with_pw(data)
    else:   # If user did not enter a new password
        data = {
            "id": session["user_id"],
            "about_me": request.form["about_me"],
            "experience_level": request.form["experience"]
        }

        User.update_without_pw(data)

    return redirect("/profile")

# -- Logs user out --
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
