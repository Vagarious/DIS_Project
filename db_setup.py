from helpers.db import *
from string import Template
from werkzeug.security import generate_password_hash

# Below is the section to run the database initialisation
db_init_path = 'sql_dll\\db_init.sql'

with open(db_init_path, 'r') as fp:
    db_init = fp.read()

# Below is the section to run creation of members
members_path = 'sql_dll\\members.sql'

with open(members_path, 'r') as fp:
    query = fp.read()

members = Template(query).substitute(
    password1 = generate_password_hash('123')
)

# Below is the section to run creation of clubs
clubs_path = 'sql_dll\\clubs.sql'
with open(clubs_path, 'r') as fp:
    clubs = fp.read()

# Below is the section to run creation of events
events_path = 'sql_dll\\events.sql'
with open(events_path, 'r') as fp:
    events = fp.read()

# Below is the section to run creation of user signups
member_events_path = 'sql_dll\\member_events.sql'
with open(member_events_path, 'r') as fp:
    member_events = fp.read()

# Below is the section to add rights to users
member_rights_path = 'sql_dll\member_rights.sql'
with open(member_rights_path, 'r') as fp:
    member_rights = fp.read()

# Below is the section to run creation of the different regions
region_nordjylland_path = 'sql_dll\\regions\\region_nordjylland.sql'
with open(region_nordjylland_path, 'r') as fp:
    region_nordjylland = fp.read()

region_midtjylland_path = 'sql_dll\\regions\\region_midtjylland.sql'
with open(region_midtjylland_path, 'r') as fp:
    region_midtjylland = fp.read()

region_syddanmark_path = 'sql_dll\\regions\\region_syddanmark.sql'
with open(region_syddanmark_path, 'r') as fp:
    region_syddanmark = fp.read()

region_sjælland_path = 'sql_dll\\regions\\region_sjælland.sql'
with open(region_sjælland_path, 'r') as fp:
    region_sjælland = fp.read()

region_hovedstaden_path = 'sql_dll\\regions\\region_hovedstaden.sql'
with open(region_hovedstaden_path, 'r') as fp:
    region_hovedstaden = fp.read()

# Below is the section to run creation of view memberships
vw_memberships_path = 'sql_dll\\vw_memberships.sql'

with open(vw_memberships_path, 'r') as fp:
    vw_memberships = fp.read()

# Below is the section to run creation of view signups
vw_signups_path = 'sql_dll\\vw_signups.sql'

with open(vw_signups_path, 'r') as fp:
    vw_signups = fp.read()

# Below is the section to run creation of view for events that need confirmation
vw_events_need_confirmation_path = 'sql_dll\\vw_events_need_confirmation.sql'

with open(vw_events_need_confirmation_path, 'r') as fp:
    vw_events_need_confirmation = fp.read()

# Below is the section to run creation of view for events that have confirmation
vw_events_with_confirmation_path = 'sql_dll\\vw_events_with_confirmation.sql'

with open(vw_events_with_confirmation_path, 'r') as fp:
    vw_events_with_confirmation = fp.read()

# Below is the section to run creation of view for events for the overview
vw_events_for_overview_path = 'sql_dll\\vw_events_for_overview.sql'

with open(vw_events_for_overview_path, 'r') as fp:
    vw_events_for_overview = fp.read()

# Below is the section to run creation of functions and triggers
functions_and_triggers_path = 'sql_dll\\functions_and_triggers.sql'
with open(functions_and_triggers_path, 'r') as fp:
    functions_and_triggers = fp.read()

conn = get_db_connection()
cur = conn.cursor()
cur.execute(db_init)
cur.execute(members)
cur.execute(clubs)
cur.execute(events)
cur.execute(member_events)
cur.execute(member_rights)
cur.execute(region_nordjylland)
cur.execute(region_midtjylland)
cur.execute(region_syddanmark)
cur.execute(region_sjælland)
cur.execute(region_hovedstaden)
cur.execute(vw_memberships)
cur.execute(vw_signups)
cur.execute(vw_events_need_confirmation)
cur.execute(vw_events_with_confirmation)
cur.execute(vw_events_for_overview)
cur.execute(functions_and_triggers)
conn.commit()
cur.close()
conn.close()
