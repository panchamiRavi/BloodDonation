from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'asdsdfsdfs13sdf_df%&'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blood_donation'

mysql = MySQL(app)

@app.route('/')
def home_page():
    return render_template("home.html")


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


@app.route('/adlogin', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('adminhome.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('admin.html', msg = msg)

@app.route("/adlogout")
def logout():
	session['loggedin']=False
	return render_template("home.html")

@app.route("/adminhome")
def adminhome_page():
    return render_template("adminhome.html")

@app.route("/viewdonar")
def viewdonar_page():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM user_reg ')
	data = cursor.fetchall()
	print(data)
	mysql.connection.commit()
	return render_template('viewdonar.html',data = data)


@app.route("/userreg")
def userreg_page():
	return render_template("userreg.html") 


@app.route('/donarreg', methods =['GET', 'POST'])
def donarreg_page():
	msg = ''
	if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'dob' in request.form and 'gender' in request.form and 'bgrup' in request.form and 'ldodate' in request.form and 'pnumber' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'zip' in request.form and 'country' in request.form:
		fname = request.form['fname']
		lname = request.form['lname']
		dob = request.form['dob']
		gender = request.form['gender']
		bgrup = request.form['bgrup']
		ldodate = request.form['ldodate']
		pnumber = request.form['pnumber']
		email = request.form['email']
		address = request.form['address']
		city = request.form['city']
		zip = request.form['zip']
		country = request.form['country']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user_reg WHERE email = % s AND pnumber = % s', (email, pnumber))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', pnumber):
			msg = 'PhoneNumber must contain only numbers !'
		elif not email or not pnumber:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO user_reg VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (fname,lname,dob,gender,bgrup,ldodate,pnumber,email,address,city,zip,country ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('userreg.html', mssg = msg)

@app.route("/donar")
def donar_page():
    return render_template("donar.html")

@app.route('/donarsearch', methods =['GET', 'POST'])
def donar_search():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM user_reg')
	data = cursor.fetchall()
	print(data)
	mysql.connection.commit()
	return render_template('donarsearch.html',data = data)

@app.route('/contact')
def contact_page():
    return render_template("contact.html")

if __name__ == '__main__':
	app.run(debug=True)
