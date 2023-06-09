# DIS_Project

For developing the webapplication as part of the project for DIS.

# Running the Web-App

Assumes a working Python 3 installation (with `python`=`python3` and `pip`=`pip3`).
Also assumes that a PostgreSQL database has been created

1. Open terminal and navigate to solution-folder

2. Create virtual environment
   ```
   python -m venv venv
   ```
3. Activate virtual environment
   ```
   .\venv\Scripts\activate
   ```
4. Install dependencies in the virtual environment
   ```
   pip install -r requirements.txt
   ```
5. Database initialization

   1. Set the database name and user in the `helpers/db.py`
   2. Run `db_setup.py`
      ```
      python db_setup.py
      ```

6. Run wep-app
   ```
   python app.py
   ```

Now the application is running, and you can open http://localhost:5000/ in a browser

# Users

The database should be initialized with three users:
camillapasser@gmail.com,
sofie@andersen.dk, and
admin@test.dk

These are the three usernames, all with password '123'.

The first user is administrator for the club 'Teitur'.
The second user is a member of the club 'Hrimnir Vestskoven'.
The third user is a global_admin.

Users (due to right-issues called members) can sign up for events created for the club of which they are a member.

Administrators can see which members are a member of the club they administrate, and can create events for that club.

Global_admins can see and do everything.

# Club overview

It is possible to see all clubs (and events for that club) without being logged in.
However, you are not able to join a club, without being logged in.

# Event overview

It is possible to see all events without being logged in.
However, to sign up for an event you must be a member of the club hosting the event, and not already signed up for the event.

# Events

All events has a date for when the period possible to sign up for the event begins, and the last day the period is active.
It is possible to set times marking the beginning and end times for an event, but is not required.
It is also possible to set a limitation on the maximum amount of participants. If this is not set, then there's no limitation of participants.
When a member signs up for an event, a row is created in member_events linking the member and the event.
However, the member needs to confirm the sign-up, before the row in member_events is updated to confirmed, and a date is set for the confirmation.
