from flask import Flask
from flask import render_template
from flask import request,redirect
from flask_cors import CORS
import psycopg2
import dbms_postgres as db
from json import dumps


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')

@app.route('/signin', methods=['GET' , 'POST'])
def signin():
    if request.method == "GET":
        return render_template('signinpage.html')
    elif request.method == "POST":
        username = dict(request.form)['username']
        password = dict(request.form)['password']
        if db.verifyUser(username,password,db.c):
            dlno = db.get_dlno(username,db.c)
            try:
                transactions = db.view_bookings(username,db.c)
                print(len(transactions))
            except:
                transactions = []
            return render_template('dashboard.html',listfiles = [(username,dlno,password)],transactions=transactions,username=username,password=password)
        else:
            return render_template('single_statement.html',inputtext="No such user found! ")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == "GET":
		return render_template('signuppage.html')
	if request.method == "POST":
		print(request.form)
		db.c , db.conn, exists = db.insertNewCustomer(dict(request.form) , db.c , db.conn)
		if exists:
			return render_template('single_statement.html',inputtext="Username already exists!")
		else:
			return render_template('single_statement.html',inputtext="Successfully created!")
		

 
@app.route('/newbooking',methods=['GET','POST'])
def newbooking():
    if request.method=='GET':
        return redirect('/signin')
    if request.method=='POST':
        username = dict(request.form)['username']
        return render_template('newbooking.html',username=username)

@app.route('/selectcar',methods=['GET','POST'])
def selectcar():
    if request.method=='GET':
        return redirect('/signin')
    if request.method=='POST':
        tab,db.c,db.conn = db.getAvailableCars(dict(request.form),db.c,db.conn)
        return render_template('selectcar.html', cars = tab,booking_details = dict(request.form))


@app.route('/cnfbooking',methods=['GET','POST'])
def cnfbooking():
    if request.method=='GET':
        return redirect('/signin')
    if request.method=='POST':
        try:
            db.c,db.conn = db.bookCar(dict(request.form),db.c,db.conn)
            return redirect('/billing')
        except:
            return render_template('finalbillingerror.html',inputtext="Error Booking Car!")


@app.route('/billing',methods=['GET','POST'] )
def billing():
	if request.method=='GET':
		return render_template('cardpayment.html')
		
@app.route('/ThankYou',methods=['GET','POST'] )
def checkout():
	if request.method=='GET':
		return render_template('ThankYou.html')


app.run(host = '0.0.0.0', port = 4000, debug = 1)


