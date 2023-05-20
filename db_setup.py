from db import *
from string import Template
from werkzeug.security import generate_password_hash

# Below is the section to run the database initialisation
db_init_path = 'db_init.sql'

with open(db_init_path, 'r') as fp:
    init_sql = fp.read()

query = Template(init_sql).substitute(
    password1 = generate_password_hash('123')
)

# Below is the section to run creation of view memberships
vw_memberships_path = 'sql_dll\\vw_memberships.sql'

with open(vw_memberships_path, 'r') as fp:
    vw_memberships = fp.read()

# Below is the section to run creation of view signups
vw_signups_path = 'sql_dll\\vw_signups.sql'

with open(vw_signups_path, 'r') as fp:
    vw_signups = fp.read()

conn = get_db_connection()
cur = conn.cursor()
cur.execute(query)
cur.execute(vw_memberships)
cur.execute(vw_signups)
conn.commit()
cur.close()
conn.close()
