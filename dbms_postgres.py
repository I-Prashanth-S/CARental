#%%
# import numpy as np
import psycopg2
import datetime
from json import dumps
import os



conn = psycopg2.connect(database = 'mydb',user="postgres", password="qwerty123",host="127.0.0.1", port="5432")
c = conn.cursor()

# % Table Viewer
def viewTable(c,table_name):
	cmd = '''  select * from {}  '''.format(table_name)
	c.execute(cmd)
	tab = c.fetchall()
	for row in tab:  print(row)

# %%
def reconnectDB(c,conn):
	conn.commit()
	conn.close()
	conn = psycopg2.connect(database = 'mydb',user="postgres", password="qwerty123",host="127.0.0.1", port="5432")
	c = conn.cursor()
	return c,conn

c,conn = reconnectDB(c,conn)

#%    Execute command from file
def executeFile(fn,c,conn):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	file = open(dir_path+'/SQLcmds/{}'.format(fn)).read()
	cmds = file.split(';')
	for cmd in cmds[:-1]:
		try:		
			c.execute(cmd)
		except Exception as exc:
			c,conn = reconnectDB(c,conn)
			print(cmd)
			print(exc)
	return c,conn

def executeCMD(cmd,c,conn):
	try:
		c.execute(cmd)
		c,conn = reconnectDB(c,conn)
	except Exception as e:
		print(e)
	return c,conn	

def insertDict(dic,table_name , c , conn):
    c.execute("Select * FROM {}".format(table_name))
    attributes = [desc[0] for desc in c.description]
    # print(attributes)
    txt = ""
    for atr in attributes:
        if dic.__contains__(atr) and dic[atr]!="":
            txt = txt + "'{}',".format(dic[atr])
        else:
            txt = txt + "null,"
    cmd = 'insert into {} values({})'.format(table_name,txt[:-1])
    c.execute(cmd)
    c,conn = reconnectDB(c,conn)
    return c,conn

def refreshDB(c,conn):
	c,conn  = executeFile('dropper.sql' , c, conn)
	c,conn = executeFile('create.sql' , c, conn)
	c,conn = executeFile('insert.sql', c, conn)
	c,conn = reconnectDB(c,conn)
	print("DB refreshed")
	return c,conn

#%%

def verifyUser(username,password,c):
    cmd = '''  select * from customer'''
    c.execute(cmd)
    tab = c.fetchall()
    for row in tab:
        if row[0] == username and row[2]==password:
            return True 
    return False    


def view_bookings(username,mycursor):
    try:
        search_all_bookings = ("SELECT car_registration_no,bill_date,booking_id, booking_status,pickup_date  FROM booking where username='{}'".format(username))
        mycursor.execute(search_all_bookings)
        output = mycursor.fetchall()
        newlist = []
        for x in output:
            newlist.append([x[0],x[1],x[2],x[3],x[4]])
        return newlist
    except Exception as e:
        print(e,"Error in SQL. Please contact admin")
        return None

def insertNewCustomer(dic , c , conn):
    username = dic['username']
    cmd = '''  select * from customer'''
    c.execute(cmd)
    tab = c.fetchall()
    for row in tab:
        if row[0] == username:
            return c, conn, True 
    c,conn = insertDict(dic, 'customer' ,c,conn)
    driving_license_no = dic['driving_license_no']
    cmd = '''  select * from customer_identity'''
    c.execute(cmd)
    tab = c.fetchall()
    for row in tab:
        if row[0] == driving_license_no:
            return c, conn, False

    c,conn = insertDict(dic, 'customer_identity' ,c,conn)
    if dic['phonenumber1']!=None and dic['phonenumber1']!="":
        ph_dict1 = {'driving_license_no' : driving_license_no, 'phone_no':dic['phonenumber1'] }
        c,conn = insertDict(ph_dict1, 'customer_phone' ,c,conn)
    if dic['phonenumber2']!=None and dic['phonenumber2']!="":
        ph_dict2 = {'driving_license_no' : driving_license_no, 'phone_no':dic['phonenumber2'] }
        c,conn = insertDict(ph_dict2, 'customer_phone' ,c,conn)
    
    return c, conn, False 

def get_dlno(username,c):
    cmd = '''  select * from customer'''
    c.execute(cmd)
    tab = c.fetchall()
    for row in tab:
        if row[0] == username:
            return row[1]


def getAvailableCars(dic,c,conn):
    category = dic['category']
    try:
        cmd = '''  select * from car where Availability_status = 'Yes' and category = '{}'  '''.format(category)
        c.execute(cmd)
        tab = c.fetchall()
    except Exception as e:
        print(e)
        c,conn = reconnectDB(c,conn)
        tab = [e]
    return tab,c,conn

def getAvailablityStatus(car_registration_no,c):
    cmd = '''  select Availability_status from car where car_registration_no  = '{}'  '''.format(car_registration_no)
    c.execute(cmd)
    Availability_status = c.fetchall()
    # print(Availability_status)
    if Availability_status[0][0] == 'Yes':
        return True
    else:
        return False

def getBookingID(c):
    cmd = '''  select * from booking'''
    c.execute(cmd)
    tab = c.fetchall()
    mx = 0
    for row in tab: mx = max(int(row[4]),mx) + 1
    return mx

def bookCar(dic,c,conn):
    
    date_of_rental = datetime.date.today().strftime("%d/%m/%Y")
    # bill_time = datetime.datetime.now().strftime("%H:%M:%S")
    booking_id = str(getBookingID(c))
    dic.update({
                        'booking_id' : booking_id,
                        'date_of_rental' : date_of_rental,
                        'booking_status' : 'Yes'
                    })
    car_registration_no = dic['car_registration_no']
    if getAvailablityStatus(car_registration_no,c):
        cmd = ''' update car set availability_status = 'No' where car_registration_no = '{}'  '''.format(car_registration_no)
        c,conn = executeCMD(cmd,c,conn)
        c,conn = insertDict(dic , 'booking' , c, conn)
    return  c,conn


#%%



c,conn = refreshDB(c,conn)