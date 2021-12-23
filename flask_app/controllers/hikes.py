from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.hike import Hike
from flask_app.models.comment import Comment
from flask_app.models.favorite import Favorite

# -- Form to create a new hike posting -- 
@app.route("/new/hike")
def add_hike():
    if "user_id" not in session: 
        return redirect("/logout")
    
    data = {
        "id": session["user_id"]
    }
    return render_template("new_hike.html", user = User.get_by_id(data))

# -- Process user input on "Create a Hike" form --
@app.route("/create/hike", methods=["POST"])
def create_hike():
    # Validate user input
    if not Hike.validate_hike(request.form):
        return redirect("/new/hike")

    Hike.save(request.form)
    return redirect("/dashboard")

# -- Edits an existing hike post --
@app.route("/edit/hike/<int:hike_id>")
def edit_hike(hike_id):
    if "user_id" not in session:
        return redirect("/logout")
    
    user_data = {
        "id": session["user_id"]
    }

    hike_data = {
        "id": hike_id
    }

    return render_template("edit_hike.html", user = User.get_by_id(user_data), hike = Hike.get_one(hike_data))

# -- Process user input on form to update existing hike post --
@app.route("/update/hike/<int:hike_id>", methods=["POST"])
def update_hike(hike_id):
    data = {
        "id": hike_id
    }

    if not Hike.validate_hike(request.form):
        return redirect(url_for("edit_hike", hike_id = hike_id))

    Hike.update(data)
    return redirect("/dashboard")

# -- Shows individual hike post --
@app.route("/view/hike/<int:hike_id>")
def view_hike(hike_id):
    if "user_id" not in session:
        return redirect("/logout")
    
    hike_data = {
        "id": hike_id
    }

    user_data = {
        "id": session["user_id"]
    }

    return render_template("view_hike.html", hike = Hike.get_one(hike_data), user = User.get_by_id(user_data), current_user = User.get_user_faves(user_data), current_hike = Hike.get_with_comments(hike_data), all_users = User.get_all())

# -- Processes user input on "Comments" form --
@app.route("/create/comment/<int:hike_id>", methods=["POST"])
def create_comment(hike_id):
    hike_data = {
        "id": hike_id
    }

    user_data = {
        "id": session["user_id"]
    }

    if not Comment.validate_comment(request.form):
        return redirect(url_for("view_hike", hike_id = hike_id))
    
    data = {
        "message": request.form["message"],
        "user_id": session["user_id"],
        "hike_id": hike_id
    }

    Comment.save(data)

    return redirect(url_for("view_hike", hike_id = hike_id))

# -- Deletes hike post from database -- 
@app.route("/delete/hike/<int:hike_id>")
def delete_hike(hike_id):
    data = {
        "id": hike_id
    }
    Hike.delete(data)
    return redirect("/dashboard")

# -- Adds a hike to user's favorites -- 
@app.route("/add_favorites/<int:hike_id>")
def add_to_favorite(hike_id):
    data = {
        "user_id": session["user_id"],
        "hike_id": hike_id
    }

    Favorite.add_to_favorite(data)

    return redirect(url_for("view_hike", hike_id = hike_id))
