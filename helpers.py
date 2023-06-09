from datetime import date
from db import *
from classes import *


def make_list_of_clubs(query_result):
    clubs = []
    for row in query_result:
        clubs.append(Club(row))
    return clubs

def make_list_of_events(query_result):
    events = []
    for row in query_result:
        events.append(Event(row))
    return events

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

def string_append(source, input):
	("Source: %d", source)
	if bool(source):
		return (source + ", " + input)
	else:
		return input
	
def signup_for_event_is_open(event):
	return event.signup_opens <= date.today() <= event.signup_closes

def determine_signup_status_for_event(event):
	open = False
	# If there is a limit for number of participants
	if event.max_spots is not None and not event.is_cancelled:
		# Check that date is within period, and that there are remaining spots
		if signup_for_event_is_open(event) and event.max_spots > 0:
			open = True
	else:
		# Check that date is within period
		if signup_for_event_is_open(event) and not event.is_cancelled:
			open = True
	return open