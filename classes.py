class Club(tuple):
    def __init__(self, club_data):
        self.club_id = club_data[0]
        self.info = club_data[1]
        self.name = club_data[2]
        self.zipcode = club_data[3]
        self.city = club_data[4]
        self.email = club_data[5]
        self.website = club_data[6]

class Event(tuple):
    def __init__(self, event_data):
        self.event_id = event_data[0]
        self.name = event_data[1]
        self.info = event_data[2]
        self.max_spots = event_data[3]
        self.date_from = event_data[4]
        self.date_to = event_data[5]
        self.time_from = event_data[6]
        self.time_to = event_data[7]
        self.signup_opens = event_data[8]
        self.signup_closes = event_data[9]
        self.price = event_data[10]
        self.club_id = event_data[11]
        self.address = event_data[12]
        self.zipcode = event_data[13]
        self.city = event_data[14]
        self.country = event_data[15]
        self.is_cancelled = event_data[16]
        self.participants = event_data[17]

class Event_wo_confirmation(tuple):
    def __init__(self, data):
        self.user_id = data[0]
        self.event_id = data[1]
        self.event_name = data[2]
        self.user_name = data[3]
        self.club_name = data[4]
        self.price = data[5]

class Event_w_confirmation(tuple):
    def __init__(self, data):
        self.user_id = data[0]
        self.event_id = data[1]
        self.name = data[2]
        self.event_name = data[3]
        self.club_name = data[4]
        self.is_confirmed = data[5]

class User(tuple):
    def __init__(self, data):
        self.email = data[0]
        self.first_name = data[1]
        self.password = data[2]
        self.name = data[3]
        self.city = data[4]
        self.country = data[5]
        self.user_id = data[6]

class SignUps(tuple):
    def __init__(self, data):
        self.user_id = data[0]
        self.event_name = data[1]
        self.name = data[2]
        self.signup_date = data[3]

class Membership(tuple):
    def __init__(self, data):
        self.user_id = data[0]
        self.number = data[1]
        self.name = data[2]
        self.club = data[3]
        self.status = data[4]
        self.expiration = data[5]