from helpers.classes import *
from datetime import date
from helpers.db import *
from werkzeug.security import check_password_hash

def create_user(firstname, lastname, gender, birthdate, country, address, zipcode, city, email, password, phone):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
			"""
			INSERT INTO member (first_name, last_name, gender, birth_date, country, address, zipcode, city, email, password, phone)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
			(firstname, lastname, gender, birthdate, country, address, zipcode, city, email, password, phone)
		)
    
    conn.commit()
    cur.close()
    conn.close()
    
    return

def user_exists(username):
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
			""".format(username)
		)
    cur.close()
    conn.close()
    
    return cur.rowcount > 0

def get_user(username):
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
			""".format(username)
		)
    user = User(cur.fetchone())
    cur.close()
    conn.close()
    
    return user

def login_user(username, password):
    if user_exists(username):
        user = get_user(username)
        if check_password_hash(user.password, password):
            return user
        else:
            return False
    else:
        return False
    
def get_signups(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
		"SELECT * FROM signups WHERE user_id = {}"
		.format(user_id)
	)
    events = cur.fetchall()
    signUps = []
    for event in events:
        signUps.append(SignUps(event))
    cur.close()
    conn.close()
    
    return signUps

def get_memberships(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
		"SELECT * FROM memberships WHERE user_id = {}"
		.format(user_id)
	)
    results = cur.fetchall()
    memberships = []
    for membership in results:
        memberships.append(Membership(membership))
    cur.close()
    conn.close()
    
    return memberships

def get_events_that_need_confirmation(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM events_need_confirmation WHERE user_id = {}"
        .format(user_id)
    )
    results = cur.fetchall()
    events = []
    for event in results:
        events.append(Event_wo_confirmation(event))
    
    return events

def confirm_events(user_id, event_ids):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE member_events
        SET is_confirmed = true, date_for_signup = '{date}'
        WHERE user_id = {user_id} AND event_id IN ({ids})
        """.format(date=date.today(), user_id = user_id, ids = event_ids)
    )
    conn.commit()
    cur.execute(
        "SELECT * FROM events_with_confirmation WHERE user_id = {user_id} AND event_id IN ({ids})"
        .format(user_id = user_id, ids = event_ids)
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    confirmations = []
    for row in result:
        confirmations.append(Event_w_confirmation(row))
    
    return confirmations