from helpers.helpers import *

def create_event(title, desc, max_spots, date_from, date_to, time_from, time_to, signup_opens, signup_closes, price, club_id, address, zipcode, city, country):
    # Check the variables which are allowed to be null
    if not bool(max_spots):
        max_spots = "null"
    if bool(time_from):
        time_from = "'" + time_from + "'"
    else:
        time_from = "null"
    if bool(time_to):
        time_to = "'" + time_to + "'"
    else:
        time_to = "null"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO event(name, info, max_spots, date_from, date_to, time_from, time_to, signup_opens, signup_closes, price, club_id, address, zipcode, city, country, is_cancelled, participants)
        VALUES ('{title}', '{desc}', {max_spots}, '{date_from}', '{date_to}', {time_from}, {time_to}, '{signup_opens}', '{signup_closes}', {price}, {club_id}, '{address}', {zipcode}, '{city}', '{country}', false, 0)
        """
        .format(title = title,
                desc = desc,
                max_spots = max_spots,
                date_from = date_from,
                date_to = date_to,
                time_from = time_from,
                time_to = time_to,
                signup_opens = signup_opens,
                signup_closes = signup_closes,
                price = price,
                club_id = club_id,
                address = address,
                zipcode = zipcode,
                city = city,
                country = country)
    )
    conn.commit()
    cur.close()
    conn.close()

    return

def get_event_info(event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM event WHERE event_id = {id}"
        .format(id = event_id))
    event = Event(cur.fetchone())
    cur.close()
    conn.close()

    return event

def get_registration_status(user_id, event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT is_confirmed FROM member_events WHERE user_id = {user_id} AND event_id = {event_id}"
        .format(user_id = user_id, event_id = event_id)
    )
    status = cur.fetchone()
    cur.close()
    conn.close()
    if status is None:
        return None
    elif status[0] is False:
        return False
    elif status[0]:
        return True
    
def sign_up_for_event(user_id, event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Conditional insert
    cur.execute(
        """
        INSERT INTO member_events(user_id, event_id, is_confirmed)
        SELECT {user_id}, {event_id}, false
        WHERE NOT EXISTS (
            SELECT 1 FROM member_events WHERE user_id = {user_id} AND event_id = {event_id}
        )
        """.format(user_id = user_id, event_id = event_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return

def get_event_participants(event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT CONCAT(first_name, ' ', last_name)
        FROM member_events
        INNER JOIN member ON member_events.user_id = member.user_id
        WHERE event_id = {id}
        """.format(id = event_id)
    )
    participants = cur.fetchall()
    # If there are participants, return only list of names
    if participants:
        participants = participants[0]
    
    return participants

def get_all_events():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM events_for_overview"
    )
    result = cur.fetchall()
    events = make_list_of_events_for_overview(result)

    return events

def search_events_by_text(text):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM events_for_overview
        WHERE LOWER(name) like LOWER('%{text}%') OR
        zipcode::TEXT = '%{text}%' OR
        LOWER(city) like LOWER('%{text}%')
        """
        .format(text = text)
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    events = make_list_of_events_for_overview(result)

    return events

def search_events_by_region(region):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM events_for_overview
        WHERE zipcode IN (
            SELECT zipcode FROM region_{region}
        )
        """.format(region = region)
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    events = make_list_of_events_for_overview(result)

    return events

def search_events_by_text_and_region(text, region):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM events_for_overview
        WHERE
        (LOWER(name) like LOWER('%{text}%') OR
        zipcode::TEXT = '%{text}%' OR
        LOWER(city) like LOWER('%{text}%'))
        AND
        (zipcode IN (
            SELECT zipcode FROM region_{region}
        ))
        """.format(text = text, region = region)
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    events = make_list_of_events_for_overview(result)

    return events