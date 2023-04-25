import os

import xml.etree.ElementTree as ET
import requests
from urllib.parse import urlparse
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from added_code import err_mesg, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

#fuction that gather and displays the information on the index page
@app.route("/", methods=["GET","POST"])
@login_required
def index():

    #line used to pull chad data from then database
    chats = db.execute("""SELECT otaku.username, chats.comment FROM chats
    INNER JOIN otaku ON chats.user=otaku.id """)

    if request.method == "POST":
        #stores the url api query
        url = 'https://cdn.animenewsnetwork.com/encyclopedia/nodelay.api.xml?title=~'

        #gets the anime name from user
        a_name = request.form.get("anime_search")

        #adds the user input to the url query
        url_update= url + a_name

        #get the reponse from the get request to the url
        response = requests.get(url_update)

        #get the actual content/data from the reponse
        r = response.content

        #gets the data as a string
        anime_info = ET.fromstring(r)

        print(anime_info)
        if anime_info.find("no results for title") == -1:
            return err_mesg("index.html","No anime found", "error")

        anime_details= []

        pic  = title = plot = None
        #loop used to iterate over each tag under anime
        for anime_node in anime_info.findall('anime'):
            #nested loop used to iterate over each tage under info
            for tag in anime_node.findall('info'):

                #expression used to store tag discriptions
                value = tag.attrib['type']

                if value == 'Main title':
                    #expression used to print the data that is within the tag eg:name of anime
                    title = tag.text

                #bool used to check any tag that contained a picture
                if value == 'Picture':
                    #expression used to store the url for the image of the anime
                    pic = tag.attrib['src']


                #bool used to check any tag that contained the plot
                if value == "Plot Summary":
                    #expression used to print the data that is within the tag eg:dsummerization of plot
                    plot = tag.text

            #line used to store anime information returned from api to dic
            anime_details.append({'title': title, 'pic': pic, 'plot': plot})

        #return statement used to pass anime details and chat details to index template
        return render_template("index.html", anime_details = anime_details, chats = chats)

    else:
        #return used to pass chats to index template
        return render_template("index.html", chats = chats)


#Fuction that governs the login rpocess for the user
@app.route("/login", methods=["GET","POST"])
def login():

    #line used to remove any previous sessions
    session.clear()

    #bool used to listen for post requests
    if request.method == "POST":

        #bool used to check if user id is left blank
        if not request.form.get("username"):
            # flash("Must enter username")
            return err_mesg("login.html","Must Provide Username", "error")

        #bool used to check if password is blank upon submit
        elif not request.form.get("password"):
            # flash("Must enter password", catagory="error")
            return err_mesg("login.html", "Must Provide Password", "error")

        #line used to check if user exists in database
        valid_user_check = db.execute("Select * FROM otaku WHERE username = ?",
        request.form.get("username"))

        #bool used to check if correct password is enter that matches password in data base.
        if len(valid_user_check) != 1 or not check_password_hash(valid_user_check[0]["hash"],
        request.form.get("password")):
             return err_mesg("login.html","Invalid Username and/or Password", "error")

        #line used to save the current user
        session["user_id"] = valid_user_check[0]["id"]

        #line used to carry user to index
        return redirect("/")

    else:
        #line used to display login template
        return render_template("login.html")

#function used to log out of the webapp
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#function used to capture and display the user's account details
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():

    #line used to get user account details from database
    user_info = db.execute("""SELECT username,f_name, l_name, dob
    FROM otaku WHERE id = :user_id""", user_id= session["user_id"])

    #loop name, username, date of birth from database results
    for user in user_info:
        info = user

    if request.method =="POST":

        #bool used to check if a new username was entered
        if request.form.get("user_n") != info["username"] and request.form.get("user_n") != None and request.form.get("user_n"):
            db.execute("UPDATE otaku SET username =:update WHERE id = :user_id", user_id = session["user_id"], update = request.form.get("user_n"))

        #bool used to check if a the users first name was updated
        if request.form.get("fname") != info["f_name"] and request.form.get("fname") != None and request.form.get("fname"):
            db.execute("UPDATE otaku SET f_name =:update WHERE id = :user_id", user_id = session["user_id"], update = request.form.get("fname"))

        #bool used to check if the users last name was updated
        if request.form.get("lname") != info["l_name"] and request.form.get("lname") != None and request.form.get("lname"):
            db.execute("UPDATE otaku SET l_name =:update WHERE id = :user_id", user_id = session["user_id"], update = request.form.get("lname"))

        #bool used to check if date of birth was updated
        if request.form.get("dateofbirth") != info["dob"] and request.form.get("dateofbirth") != None and request.form.get("dateofbirth"):
            db.execute("UPDATE otaku SET dob =:update WHERE id = :user_id", user_id = session["user_id"], update = request.form.get("dateofbirth"))

        #bool used to display account template and pass user info
        return render_template("account.html", user = info)

    else:
        #bool used to display account template  and pass user info
        return render_template("account.html", user = info)


#function used to handle new user registration
@app.route("/registration", methods=["GET", "POST"])
def registration():

    #bool used to listen for post requests
    if request.method =="POST":

        #bool used to check if username is left blank upon submission
        if not request.form.get("username"):
            # flash("You must enter a username")
            return err_mesg("registration.html","You must enter a username", "error")

        #line used to pull all usernames within database
        user_n = db.execute("Select * FROM otaku WHERE username = :name", name=request.form.get("username"))

        #bool used to check if username is entered is already used
        if user_n == None:
            return err_mesg("registration.html","Username Already Taken", "error")

        #bool used to check if first name has been left blank on submit
        elif not request.form.get("f_name"):
            # flash("Cannot leave first name blank")
            return err_mesg("registration.html","Cannot leave first name blank", "error")

        #bool used to check if last name has been left blank on submit
        elif not request.form.get("l_name"):
            # flash("You must Cannot leave last name blank", 403)
            return err_mesg("registration.html","Cannot leave last name blank", "error")

        #bool used to check if birthday has been left blank on submit
        elif not request.form.get("birthday"):
            # flash("Cannot leave birthday blank")
            return err_mesg("registration.html","Cannot leave birthday blank", "error")

        #bool used to check if password has been left blank on submit
        elif not request.form.get("password"):
            # flash("Must enter password")
            return err_mesg("registration.html","Must enter password", "error")

        #bool used to check if password has been left blank on submit
        elif not request.form.get("confirmation"):
            # flash("Must enter confirm password")
            return err_mesg("registration.html","Must confirm password", "error")

        #bool used to check if second password enters matches previous one
        elif request.form.get("password") != request.form.get("confirmation"):
            # flash("Passwords must match")
            return err_mesg("registration.html","Passwords must match", "error")

        #line used to enter new user into database
        user = db.execute("""INSERT INTO otaku (username, f_name, l_name, dob, hash)
            VALUES (:username, :f_name, :l_name, :dob, :hash)""",  username=request.form.get("username"),
            f_name=request.form.get("f_name"), l_name=request.form.get("l_name"), dob=request.form.get("birthday"),
            hash=generate_password_hash(request.form.get("password")))

        #line use to check if user eas succesfully entered into database
        if user is None:
            return err_mesg("registration.html","An Error Occured When Registering", "error")

        session["user_id"] = user

        #line used to display index page
        return redirect("/")


    else:
        #line used to display registration template
        return render_template("registration.html")


@app.route("/chat", methods=["GET","Post"])
@login_required
def chat():

    #bool used to listen for post requests
    if request.method == "POST":

        #bool used to check if chat was left blank on submit
        if not request.form.get("chats"):
            return err_mesg("index.html","Blank Comments Are Not Allowed", "error")

        #line used to store chat data
        db.execute("INSERT INTO chats (user, comment) VALUES (:user, :comment)", user=session["user_id"], comment=request.form.get("chats"))

        #line used to display index page
        return redirect("/")

    else:
        #line used to display index template
        return render_template("index.html")

#function used to update password
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():

    if request.method == "POST":

        #bool used too check if empty password was submitted
        if not request.form.get("new_password"):
            return err_mesg("password.html","New Password is Blank", "error")

         #bool used too check if empty password was submitted
        elif not request.form.get("confirmation"):
            return err_mesg("password.html","Password Confirmation is Blank", "error")

         #bool used too check if both entries for the password matches
        if request.form.get("new_password") != request.form.get("confirmation", 403):
            return err_mesg("password.html","Passwords should match", "error")

        #line used to insert update password in database
        db.execute("Update otaku SET hash = :passw WHERE id = :user", user= session["user_id"], passw =generate_password_hash(request.form.get("new_password")))

        flash("Password Updated")
        #line used to carry user to index page
        return redirect("/")

    else:
        #line used to display password template
        return render_template("password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return err_mesg(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)