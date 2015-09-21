#!/usr/bin/python
import mysql.connector as mysql
from mysql.connector import errorcode

from modules.config import apconfig 

db = None

config = {
  'user': apconfig.get("database", "user"),
  'password': apconfig.get("database", "password"),
  'host': apconfig.get("database", "host"),
  'database': apconfig.get("database", "db_name")
}

"""
This methods try to make a connection to the database using the  
parameters defined in the config object.
If any error occurs an exception is raised.
"""
def connect():
	global db
	
	if db is None:
		print("Connecting to database...")
		try:
			db = mysql.connect(**config)
		except mysql.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password!")			
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)

"""
This method close the connection to the database stored in db.
If the connection is not open, then anything happens.
"""
def disconnect():
	global db
	
	if db is not None:
		print("Disconnecting from database...")
		db.close()

"""
This method execute onto the database the query received by parameter, 
using as parameteres the values received.

Examples:

1)

->	add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
															
->	data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))
	
->	makeChange(add_employee, data_employee)

2)

->	add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

->	# Insert salary information
	data_salary = {
	  'emp_no': emp_no,
	  'salary': 50000,
	  'from_date': tomorrow,
	  'to_date': date(9999, 1, 1),
	}
	
->	makeChange(add_salary, data_salary)

"""
def makeChange(query, values):
	global db
	if db is not None:
		connect()
		cursor = db.cursor()
		cursor.execute(query, values)
		db.commit()

"""
This method execute a query against the database and return the result if 
any.

Examples:

1)
query = "SELECT * FROM network_distances"
results = makeQuery(query)

"""
def makeQuery(query):
	global db
	
	if db is not None:
		connect()
		cursor = db.cursor()
		cursor.execute(query)
		return cursor.fetchall()
	
	return None




if __name__ == '__main__':
#def test():
	connect()
	
	results = makeQuery("SELECT * FROM network_distances WHERE initial_node = 1")
	for(id, network_id, initial_node, final_node, length) in results:
		print(initial_node, final_node)
	disconnect()

""" 
See http://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

"""