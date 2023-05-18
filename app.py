from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

# Create a Flask app
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to the database using psycopg2 library and the database credentials
conn = psycopg2.connect(
	host="localhost",
	database="sportilight",
	user="postgres",
	password="!postgres2023!"
)

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

		if phone is None:
			print("No phone number is provided")
		else:
			print("Phone number: ", phone)

		cur = conn.cursor()
		cur.execute(
			"""
			INSERT INTO member (firstname, lastname, gender, birthdate, country, address, zipcode, city, email, password, phone)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
			(firstname, lastname, gender, birthdate, country, address, zipcode, city, email, _hashedPassword, phone)
		)
		conn.commit()
		return redirect("/")
	return render_template("signup.html")

@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		print(request.form["password"])
		_hashedPassword = generate_password_hash(request.form["password"])
		print(_hashedPassword)
		cur = conn.cursor()
		cur.execute(
			""" SELECT email, firstname, password FROM member
			WHERE email = '{}';
			""".format(request.form["username"])
		)
		if cur.rowcount > 0:
			user = cur.fetchone()
			cur.close()
			if check_password_hash(user[2], request.form["password"]):
				session["username"] = user[0]
				session["name"] = user[1]
				return redirect("/")
		else:
			cur.close()
			return render_template("error.html")

			
	return render_template("login.html")

if __name__ == '__main__':
	app.debug=True
	app.run()
