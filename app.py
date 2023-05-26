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
			if check_password_hash(user[2], request.form["password"]):
				session["username"] = user[0]
				session["firstname"] = user[1]
				session["name"] = user[3]
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

@app.route('/confirmation')
def confirmation():
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"SELECT * FROM events_need_confirmation WHERE user_id = {}"
		.format(session["user_id"])
	)
	res = cur.fetchall()
	events = []
	event_ids = ""
	total = 0
	for event in res:
		row = Event_wo_confirmation(event)
		events.append(row)
		event_ids = string_append(event_ids, str(row.event_id))
		total += row.price
	return render_template("confirmation.html", events=events, total=total, ids=event_ids)

def string_append(source, input):
	("Source: %d", source)
	if bool(source):
		return (source + ", " + input)
	else:
		return input

@app.route('/confirmed')
def confirmed():
	events = request.args.get('events')
	
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"""
		UPDATE member_events
		SET is_confirmed = true, date_for_signup = '{date}'
		WHERE user_id = {user_id} AND event_id IN ({ids})
		""".format(date=date.today(), user_id=session["user_id"], ids=events)
	)
	conn.commit()
	cur.execute(
		"SELECT * FROM events_with_confirmation WHERE user_id = {user_id} AND event_id IN ({event_ids})"
		.format(user_id = session["user_id"], event_ids = events)
	)
	res = cur.fetchall()
	cur.close()
	conn.close()
	confirmations = []
	for row in res:
		confirmations.append(Event_w_confirmation(row))
	return render_template("confirmed.html", events=confirmations)

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

@app.route('/clubpage/<int:club_id>/info')
def clubpage_info(club_id):
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
	return render_template('clubs/club_info.html', 
				club=club,
				future_events=future_events,
				past_events=past_events,
				today=date.today(),
				admin=user_has_administrative_rights(session.get('user_id'),club_id),
				member=user_is_member(session.get('user_id'),club_id))


@app.route('/clubpage/<int:club_id>/members')
def clubpage_members(club_id):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"SELECT * from club WHERE club_id = {}"
		.format(club_id)
	)
	club = Club(cur.fetchone())
	cur.execute(
		"""
		SELECT CONCAT(first_name, ' ', last_name) FROM member_rights
		INNER JOIN member ON member_rights.user_id = member.user_id
		WHERE club_id = {} AND right_id IN (1,2)
		""".format(club_id)
	)
	member_names = cur.fetchall()
	cur.close()
	conn.close()
	return render_template('clubs/club_members.html', 
			club=club, 
			members=member_names,
			admin=user_has_administrative_rights(session.get('user_id'),club_id),
			member=user_is_member(session.get('user_id'),club_id))

@app.route('/clubpage/<int:club_id>/join')
def clubpage_join(club_id):
	if session.get("user_id"):
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute(
			"SELECT * from club WHERE club_id = {}"
			.format(club_id)
		)
		club = Club(cur.fetchone())
		if not user_is_member(session["user_id"],club_id):
			cur.execute(
				"""
				INSERT INTO member_rights(user_id, club_id, right_id, is_active, expiration_date)
				VALUES ({user_id}, {club_id}, 1, true, '{exp_date}')
				""".format(user_id=session["user_id"],
							club_id=club_id,
							exp_date=date(date.today().year,12,31))
			)
		conn.commit()
		cur.close()
		conn.close()
		return render_template("clubs/club_join.html", club=club, member=True)
	
	flash("You must sign in, or sign up, before you can join a club", "Error")
	return redirect("/")

@app.route('/clubpage/<int:club_id>/admin',methods=["GET","POST"])
def clubpage_admin(club_id):
	user_is_admin = user_has_administrative_rights(session.get('user_id'),club_id)
	if user_is_admin:
		if request.method == "GET":
			conn = get_db_connection()
			cur = conn.cursor()
			cur.execute(
				"SELECT * from club WHERE club_id = {}"
				.format(club_id)
			)
			club = Club(cur.fetchone())
			return render_template("clubs/club_admin.html", club=club, admin=user_is_admin, member=user_is_member(session.get('user_id'),club_id))
		else:
			# Check the variables that are allowed to be null
			max_spots = request.form.get('max_participants')
			time_from = request.form.get('start_time')
			time_to = request.form.get('end_time')
			null = "null"
			if not bool(max_spots):
				max_spots = null
			if not bool(time_from):
				time_from = null
				time_to = null

			# Continue with the insertion
			conn = get_db_connection()
			cur = conn.cursor()

			if time_from == "null":
				cur.execute(
				"""
				INSERT INTO event(name,info,max_spots,date_from,date_to,time_from,time_to,signup_opens,signup_closes,price,club_id,address,zipcode,city,country,is_cancelled,participants)
				VALUES ('{title}','{desc}',{max_spots},'{date_from}','{date_to}',{time_from},{time_to},'{signup_opens}','{signup_closes}',{price},{club_id},'{address}',{zipcode},'{city}','{country}',{cancelled},{participants})
				"""
				.format(title = request.form.get('title'),
	    				desc = request.form.get('desc'),
						max_spots = max_spots,
						date_from = request.form.get('start_date'),
						date_to = request.form.get('end_date'),
						time_from = time_from,
						time_to = time_to,
						signup_opens = request.form.get('signup_opens'),
						signup_closes = request.form.get('signup_closes'),
						price = request.form.get('price'),
						club_id = club_id,
						address = request.form.get('address'),
						zipcode = request.form.get('zipcode'),
						city = request.form.get('zipcode'),
						country = request.form.get('country'),
						cancelled = False,
						participants = 0)
				)
			else:
				cur.execute(
					"""
					INSERT INTO event(name,info,max_spots,date_from,date_to,time_from,time_to,signup_opens,signup_closes,price,club_id,address,zipcode,city,country,is_cancelled,participants)
					VALUES ('{title}','{desc}',{max_spots},'{date_from}','{date_to}','{time_from}','{time_to}','{signup_opens}','{signup_closes}',{price},{club_id},'{address}',{zipcode},'{city}','{country}',{cancelled},{participants})
					"""
					.format(title = request.form.get('title'),
							desc = request.form.get('desc'),
							max_spots = max_spots,
							date_from = request.form.get('start_date'),
							date_to = request.form.get('end_date'),
							time_from = time_from,
							time_to = time_to,
							signup_opens = request.form.get('signup_opens'),
							signup_closes = request.form.get('signup_closes'),
							price = request.form.get('price'),
							club_id = club_id,
							address = request.form.get('address'),
							zipcode = request.form.get('zipcode'),
							city = request.form.get('zipcode'),
							country = request.form.get('country'),
							cancelled = False,
							participants = 0)
				)
			conn.commit()
			cur.close()
			conn.close()
			# PLEASE don't forget to change this to something meaningful...
			return redirect(url_for('clubpage_admin', club_id=club_id, member=user_is_member(session.get('user_id'),club_id)))
	flash("You shall not pass!",'Error')
	return redirect("/")

def user_has_administrative_rights(user_id, club_id):
	if user_id:
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute(
			"""
			SELECT EXISTS(SELECT 1 FROM member_rights WHERE user_id = {user_id} AND club_id = {club_id} AND right_id IN (2,3)) AS user_is_admin
			""".format(user_id=user_id, club_id=club_id)
		)
		user_is_admin = cur.fetchone()
		return user_is_admin[0]
	return False

def user_is_member(user_id, club_id):
	if user_id:
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute(
			"""
			SELECT EXISTS(SELECT 1 FROM member_rights WHERE user_id = {user_id} AND club_id = {club_id} AND right_id IN (1,2)) AS user_is_member
			""".format(user_id=user_id, club_id=club_id)
		)
		user_is_member = cur.fetchone()
		return user_is_member[0]
	return False


@app.route('/eventpage/<int:event_id>')
def eventpage(event_id):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM event WHERE event_id = {id}"
	     .format(id = event_id))
	event = Event(cur.fetchone())
	cur.close()
	conn.close()
	is_member=user_is_member(session.get("user_id"),event.club_id)
	return render_template('events/eventpage.html', event = event, member = is_member)

@app.route('/events/signup/<int:event_id>', methods=["GET","POST"])
def event_signup(event_id):
	if request.method == "GET":
		if (session.get('user_id') is None):
			flash("You must sign up or log in before signing up for events", "error")
			return redirect("/")
		else:
			conn = get_db_connection()
			cur = conn.cursor()
			cur.execute("SELECT is_confirmed FROM member_events WHERE user_id = {user_id} AND event_id = {event_id}"
	       		.format(user_id = session["user_id"], event_id = event_id)
		   	)
			registrationStatus = cur.fetchone()
			if registrationStatus is None:
				exists = False
				confirmed = False
			elif registrationStatus[0] is False:
				exists = True
				confirmed = False
			elif registrationStatus[0]:
				exists = True
				confirmed = True
			# if entry exists and is false, then the user is registered but not confirmed
			# if the entry exists and is true, then the user has confirmed the registration
			# if the entry does not exists, then the user hasn't signed up for the event and is shown the form
			cur.execute("SELECT * FROM event WHERE event_id = {id}".format(id = event_id))
			event = Event(cur.fetchone())
			cur.close()
			conn.close()
			is_member = user_is_member(session["user_id"],event.club_id)
			return render_template("events/event_signup.html", event=event, exists=exists, confirmed=confirmed, member = is_member)
	else:
		conn = get_db_connection()
		cur = conn.cursor()
		# conditional insert
		cur.execute(
		"""
		INSERT INTO member_events(user_id,event_id,is_confirmed)
		SELECT {user_id},{event_id},false
		WHERE NOT EXISTS (
			SELECT 1 from member_events WHERE user_id = {user_id} and event_id = {event_id})
		""".format(user_id = session["user_id"], event_id = event_id)
		)
		conn.commit()
		cur.execute("SELECT * FROM event WHERE event_id = {id}".format(id = event_id))
		event = Event(cur.fetchone())
		cur.close()
		conn.close()
		is_member = user_is_member(session.get("user_id"),event.club_id)
		return render_template('events/event_signup.html', event=event, exists=True, confirmed=False, member = is_member)

@app.route('/events/participants/<int:event_id>')
def event_participants(event_id):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"""
		SELECT CONCAT(first_name, ' ', last_name)
		FROM member_events
		INNER JOIN member ON member_events.user_id = member.user_id
		WHERE event_id = {id}
		""".format(id=event_id)
		)
	participants = cur.fetchall()
	if participants:
		participants = participants[0]
	cur.execute("SELECT * FROM event WHERE event_id = {id}".format(id = event_id))
	event = Event(cur.fetchone())
	cur.close()
	conn.close()
	is_member = user_is_member(session.get("user_id"),event.club_id)
	return render_template("events/participants.html", event=event, participants=participants, member = is_member)

@app.route('/external/<path:url>', methods=["GET"])
def external(url):
	if url.startswith('www.'):
		return redirect('http://'+ url, code=302)
	else:
		return redirect(url, code=302)

if __name__ == '__main__':
	app.debug=True
	app.run()
