from db import *
from classes import *
from datetime import date
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

@app.route('/overview', methods=["GET", "POST"])
def club_overview():
	if request.method == "GET":
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute(
			"SELECT * from club"
		)
		clubs = cur.fetchall()
		list_of_clubs = []
		for club in clubs:
			list_of_clubs.append(Club(club))

		return render_template("club_overview.html", clubs=list_of_clubs)
	else:
		# Three cases
		searchText = request.form.get('search_text')
		region_selected = request.form.get('search_region')
		conn = get_db_connection()
		cur = conn.cursor()
		# Case 1: Searchtext and no region selected
		if searchText is not None and region_selected is None:
			cur.execute(
				"""
				SELECT * FROM club
				WHERE LOWER(name) like LOWER('%{search}%') OR
				zipcode::TEXT = '%{search}%' OR
				LOWER(city) like LOWER('%{search}%')
				"""
				.format(search=searchText)
			)
		# Case 2: No searchtext but region selected
		elif searchText is None and region_selected is not None:
			if region_selected == "all":
				return redirect('/overview')
			cur.execute(
				"""
				SELECT * FROM club
				WHERE zipcode IN (
					SELECT zipcode FROM region_{region}
				)
				""".format(region=region_selected)
			)
		else:
		# Case 3: Both searchtext and region selected
			if region_selected == "all":
				cur.execute(
					"""
					SELECT * FROM club
					WHERE LOWER(name) like LOWER('%{search}%') OR
					zipcode::TEXT = '%{search}%' OR
					LOWER(city) like LOWER('%{search}%')
					"""
					.format(search=searchText)
				)
			else:
				cur.execute(
					"""
					SELECT * FROM club
					WHERE
						(LOWER(name) like LOWER('%{search}%') OR
						zipcode::TEXT = '%{search}%' OR
						LOWER(city) like LOWER('%{search}%'))

						AND
		
						(zipcode IN (
							SELECT zipcode FROM region_{region}))
					""".format(search=searchText, region=region_selected)
				)
		clubs=cur.fetchall()
		list_of_clubs = []
		for club in clubs:
			list_of_clubs.append(Club(club))
		cur.close()
		conn.close()
		return render_template("club_overview.html", clubs=list_of_clubs)

@app.route('/clubpage/<int:club_id>')
def clubpage(club_id):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"SELECT * from club WHERE club_id = {}"
		.format(club_id)
	)
	club = Club(cur.fetchone())
	# Get upcomming / future events
	cur.execute(
		"""
		SELECT * FROM event WHERE club_id = {id} AND
		date_from >= '{date}'
		"""
		.format(id = club.club_id,
	  		date = date.today())
	)
	fevents = cur.fetchall()
	future_events = []
	for event in fevents:
		future_events.append(Event(event))
	# Get past events
	cur.execute(
		"""
		SELECT * FROM event WHERE club_id = {id} AND
		date_from < '{date}'
		""".format(id = club.club_id,
	     	date = date.today())
	)
	pevents = cur.fetchall()
	past_events = []
	for event in pevents:
		past_events.append(Event(event))
	cur.close()
	conn.close()
	print("Today: " + str(date.today()))
	return render_template('clubpage.html', 
			club=club,
			future_events=future_events,
			past_events=past_events,
			today=date.today())

@app.route('/external/<url>')
def external(url):
	if url.startswith('http'):
		website = url
	else:
		website = "http://" + url
	return redirect(website)

if __name__ == '__main__':
	app.debug=True
	app.run()
