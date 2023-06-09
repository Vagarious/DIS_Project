from db import *
from classes import *
from datetime import date
from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask_session import Session
from helpers import *
from queries.clubs import *
from queries.events import *
from queries.members import *
from werkzeug.security import generate_password_hash


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

		create_user(firstname, lastname, gender, birthdate, country, address, zipcode, city, email, _hashedPassword, phone)
		
		return redirect("/")
	return render_template("signup.html")

@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		user = login_user(username, password)
		if user is not False:
			session["username"] = user.email
			session["firstname"] = user.first_name
			session["name"] = user.name
			session["city"] = user.city
			session["country"] = user.country
			session["user_id"] = user.user_id
			return redirect("/")
		else:
			return render_template("error.html")

	return render_template("login.html")

@app.route('/signout', methods=["GET", "POST"])
def signout():
	if session.get("username") is None:
		flash("You must sign in before you can sign out!", "warning")
	else:
		session.clear()
	return redirect("/")


@app.route('/profile', methods=["GET", "POST"])
def profile():
	return render_template("profile/profile.html")

@app.route('/profile/events', methods=["GET", "POST"])
def profile_events():
	events = get_signups(session["user_id"])
	return render_template("profile/events.html", events=events)

@app.route('/profile/memberships', methods=["GET", "POST"])
def profile_memberships():
	memberships = get_memberships(session["user_id"])
	return render_template("profile/memberships.html", memberships=memberships)

@app.route('/confirmation')
def confirmation():
	events = get_events_that_need_confirmation(session["user_id"])
	event_ids = ""
	total = 0
	for event in events:
		event_ids = string_append(event_ids, str(event.event_id))
		total += event.price
	return render_template("confirmation.html", events=events, total=total, ids=event_ids)

@app.route('/confirmed')
def confirmed():
	events = request.args.get('events')
	confirmations = confirm_events(session["user_id"], events)
	
	return render_template("confirmed.html", events=confirmations)

@app.route('/overview', methods=["GET", "POST"])
def club_overview():
	if request.method == "GET":
		clubs = get_all_clubs()
		return render_template("club_overview.html", clubs=clubs)
	else:
		# Three cases
		searchText = request.form.get('search_text')
		region_selected = request.form.get('search_region')
		
		# Case 1: Searchtext and no region selected
		if searchText is not None and region_selected is None:
			clubs = search_clubs_by_text(searchText)
		# Case 2: No searchtext but region selected
		elif not searchText and region_selected is not None:
			if region_selected == "all":
				return redirect('/overview')
			clubs = search_clubs_by_region(region_selected)
		else:
		# Case 3: Both searchtext and region selected
			if region_selected == "all":
				clubs = search_clubs_by_text(searchText)
			else:
				clubs = search_clubs_by_text_and_region(searchText, region_selected)
		
		return render_template("club_overview.html", clubs=clubs)

@app.route('/clubpage/<int:club_id>/info')
def clubpage_info(club_id):
	club = get_club_info(club_id)
	# Get upcomming / future events
	future_events = get_upcomming_events_for_club(club.club_id)
	# Get past events
	past_events = get_past_events_for_club(club.club_id)
	return render_template('clubs/club_info.html', 
				club=club,
				future_events=future_events,
				past_events=past_events,
				today=date.today(),
				admin=user_has_administrative_rights(session.get('user_id'),club_id),
				member=user_is_member(session.get('user_id'),club_id))


@app.route('/clubpage/<int:club_id>/members')
def clubpage_members(club_id):
	club = get_club_info(club_id)
	member_names = get_club_members(club_id)
	return render_template('clubs/club_members.html', 
			club=club, 
			members=member_names,
			admin=user_has_administrative_rights(session.get('user_id'),club_id),
			member=user_is_member(session.get('user_id'),club_id))

@app.route('/clubpage/<int:club_id>/join')
def clubpage_join(club_id):
	if session.get("user_id"):
		club = get_club_info(club_id)
		if not user_is_member(session["user_id"],club_id):
			join_club(session["user_id"], club_id)
		return render_template("clubs/club_join.html", club=club, member=True)
	
	flash("You must sign in, or sign up, before you can join a club", "Error")
	return redirect("/")

@app.route('/clubpage/<int:club_id>/admin',methods=["GET","POST"])
def clubpage_admin(club_id):
	user_is_admin = user_has_administrative_rights(session.get('user_id'),club_id)
	if user_is_admin:
		if request.method == "GET":
			club = get_club_info(club_id)
			return render_template("clubs/club_admin.html", club=club, admin=user_is_admin, member=user_is_member(session.get('user_id'),club_id))
		else:
			create_event(
				request.form.get('title'),
				request.form.get('desc'),
				request.form.get('max_participants'),
				request.form.get('start_date'),
				request.form.get('end_date'),
				request.form.get('start_time'),
				request.form.get('end_time'),
				request.form.get('signup_opens'),
				request.form.get('signup_closes'),
				request.form.get('price'),
				club_id,
				request.form.get('address'),
				request.form.get('zipcode'),
				request.form.get('city'),
				request.form.get('country')
			)
			# PLEASE don't forget to change this to something meaningful...
			return redirect(url_for('clubpage_admin', club_id=club_id, member=user_is_member(session.get('user_id'),club_id)))
	flash("You shall not pass!",'Error')

	return redirect("/")

@app.route('/eventpage/<int:event_id>')
def eventpage(event_id):
	event = get_event_info(event_id)
	is_member = user_is_member(session.get("user_id"), event.club_id)
	signup_open = determine_signup_status_for_event(event)

	return render_template('events/eventpage.html', event = event, member = is_member, signup_open = signup_open)

@app.route('/events/signup/<int:event_id>', methods=["GET","POST"])
def event_signup(event_id):
	if request.method == "GET":
		if (session.get('user_id') is None):
			flash("You must sign up or log in before signing up for events", "Error")
			return redirect("/")
		else:
			event = get_event_info(event_id)
			if not determine_signup_status_for_event(event):
				flash("Event is not open for signup", "Error")
				return redirect("/")
			registrationStatus = get_registration_status(session["user_id"], event_id)
			# if the entry does not exists, then the user hasn't signed up for the event and is shown the form
			if registrationStatus is None:
				exists = False
				confirmed = False
			# if entry exists and is false, then the user is registered but not confirmed
			elif registrationStatus is False:
				exists = True
				confirmed = False
			# if the entry exists and is true, then the user has confirmed the registration
			elif registrationStatus:
				exists = True
				confirmed = True
			is_member = user_is_member(session["user_id"], event.club_id)
			return render_template("events/event_signup.html", event = event, exists = exists, confirmed = confirmed, member = is_member)
	else:
		sign_up_for_event(session["user_id"], event_id)
		event = get_event_info(event_id)
		is_member = user_is_member(session.get("user_id"),event.club_id)
		return render_template('events/event_signup.html', event=event, exists=True, confirmed=False, member = is_member)

@app.route('/events/participants/<int:event_id>')
def event_participants(event_id):
	participants = get_event_participants(event_id)
	event = get_event_info(event_id)
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
