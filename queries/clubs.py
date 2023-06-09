from datetime import date
from helpers.db import *
from helpers.helpers import *

def get_all_clubs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM club"
    )
    result = cur.fetchall()
    clubs = make_list_of_clubs(result)
    
    return clubs

def search_clubs_by_text(text):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM club
        WHERE LOWER(name) like LOWER('%{text}%') OR
        zipcode::TEXT = '%{text}%' OR
        LOWER(city) like LOWER('%{text}%') 
        """
        .format(text = text)
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    clubs = make_list_of_clubs(result)

    return clubs

def search_clubs_by_region(region):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM club
        WHERE zipcode IN (
            SELECT zipcode FROM region_{region}
        )
        """.format(region = region)
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    clubs = make_list_of_clubs(result)

    return clubs

def search_clubs_by_text_and_region(text, region):
    conn = get_db_connection()
    cur = conn.cursor()
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
		""".format(search = text, region = region)
	)
    result = cur.fetchall()
    cur.close()
    conn.close()
    clubs = make_list_of_clubs(result)

    return clubs

def get_club_info(club_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM club WHERE club_id = {}"
        .format(club_id)
    )
    club = Club(cur.fetchone())
    cur.close()
    conn.close()

    return club

def get_upcomming_events_for_club(club_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM event WHERE club_id = {id} AND
        date_from >= '{date}'
        """
        .format(id = club_id, date = date.today())
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    future_events = make_list_of_events(result)

    return future_events

def get_past_events_for_club(club_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM event WHERE club_id = {id} AND
        date_from < '{date}'
        """
        .format(id = club_id, date = date.today())
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    past_events = make_list_of_events(result)

    return past_events

def get_club_members(club_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
		"""
		SELECT CONCAT(first_name, ' ', last_name) FROM member_rights
		INNER JOIN member ON member_rights.user_id = member.user_id
		WHERE club_id = {} AND right_id IN (1,2)
		""".format(club_id)
	)
    members = cur.fetchall()
    cur.close()
    conn.close()

    return members

def join_club(user_id, club_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO member_rights(user_id, club_id, right_id, is_active, expiration_date)
        VALUES ({user_id}, {club_id}, 1, true, '{exp_date}')
        """.format(user_id = user_id,
                   club_id = club_id,
                   exp_date = date(date.today().year, 12, 31))
    )
    conn.commit()
    cur.close()
    conn.close()

    return