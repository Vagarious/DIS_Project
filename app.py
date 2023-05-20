from db import *
from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Flask app
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Root route

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
	if request.method == "POST":
		firstname = request.form["firstname"]
		lastname = request.form["lastname"]
		gender = request.form["gender"]
		birthdate = request.form["birthdate"]
		country = request.form["country"]
		address = request.form["address"]
		zipcode = request.form["zipcode"]
		city = request.form["city"]
		email = request.form["email"]
		_hashedPassword = generate_password_hash(request.form["password"])
		phone = request.form.get('phone')

		if phone is None:
			print("No phone number is provided")
		else:
			print("Phone number: ", phone)

		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute(
			"""
			INSERT INTO member (firstname, lastname, gender, birthdate, country, address, zipcode, city, email, password, phone)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
			(firstname, lastname, gender, birthdate, country, address, zipcode, city, email, _hashedPassword, phone)
		)
		conn.commit()
		cur.close()
		conn.close()
		return redirect("/")
	return render_template("signup.html")

@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute(
			""" SELECT email, 
			first_name, 
			password, 
			concat(first_name, ' ', last_name) as name,
			city,
			country,
			user_id 
			FROM member
			WHERE email = '{}';
			""".format(request.form["username"])
		)
		if cur.rowcount > 0:
			user = cur.fetchone()
			cur.close()
			conn.close()
			print("Hello")
			if check_password_hash(user[2], request.form["password"]):
				session["username"] = user[0]
				print(user[0])
				print(user[1])
				session["firstname"] = user[1]
				session["name"] = user[3]
				print(session["name"])
				session["city"] = user[4]
				session["country"] = user[5]
				session["user_id"] = user[6]
				return redirect("/")
		else:
			cur.close()
			conn.close()
			return render_template("error.html")

	return render_template("login.html")

@app.route('/signout', methods=["GET", "POST"])
def signout():
	if session["username"] is None:
		flash("You must sign in before you can sign out!", "warning")
	else:
		session.clear()
	return redirect("/")


@app.route('/profile', methods=["GET", "POST"])
def profile():
	return render_template("profile/profile.html")

@app.route('/profile/events', methods=["GET", "POST"])
def profile_events():
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"SELECT * FROM signups WHERE user_id = {}"
		.format(session["user_id"])
	)
	events = cur.fetchall()
	cur.close()
	conn.close()
	return render_template("profile/events.html", events=events)

@app.route('/profile/memberships', methods=["GET", "POST"])
def profile_memberships():
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"SELECT * FROM memberships WHERE user_id = {}"
		.format(session["user_id"])
	)
	memberships = cur.fetchall()
	cur.close()
	conn.close()
	return render_template("profile/memberships.html", memberships=memberships)

if __name__ == '__main__':
	app.debug=True
	app.run()
