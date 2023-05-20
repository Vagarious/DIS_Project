import psycopg2
# Connect to the database using psycopg2 library and the database credentials
def get_db_connection():
	conn = psycopg2.connect(
		host="localhost",
		database="sportilight",
		user="postgres",
		password="!postgres2023!"
	)
	return conn