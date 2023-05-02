from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2

# Create a Flask app
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Connect to the database using psycopg2 library and the database credentials
conn = psycopg2.connect(
	host="localhost",
	database="project_db",
	user="postgres",
	password="!postgres2023!"
)

# Root route



@app.route("/")
def index():
	if 'username' in session:
		return render_template("signed_in.html", name=session["username"])
	return render_template("index.html")


@app.route('/created', methods=['POST'])
def created():
	session['username'] = request.form['firstname']
	firstname=request.form["firstname"]
	lastname=request.form["lastname"]
	address=request.form["address"]
	zipcode=request.form["zipcode"]
	city=request.form['city']
	email=request.form["email"]
	password=request.form["password"]

	cur = conn.cursor()
	cur.execute(
		"INSERT INTO users (firstname, lastname, address, zipcode, city, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (firstname, lastname, address, zipcode, city, email, password)
	)
	conn.commit()
	cur.close()

	return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
	return render_template("signup.html")

@app.route('/login', methods=["POST"])
def login():
	return render_template("login.html")

@app.route('/signed_in', methods=["POST"])
def signed_in(name=None):
	print("username: ", request.form['username'])
	print("password: ", request.form['password'])
	cur=conn.cursor()
	cur.execute(
		""" SELECT * FROM users
		WHERE email = '{}' AND
		password = '{}';
		""".format(request.form['username'], request.form['password'])
	)
	if cur.rowcount > 0:
		result=cur.fetchone()
		nametest = result[0]
		print("nametest: ",nametest)
		return render_template("signed_in.html", name=nametest)
	return "Error"

if __name__ == '__main__':
	app.debug=True
	app.run()
