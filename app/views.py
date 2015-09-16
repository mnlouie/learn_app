from flask import render_template, request
from app import app
import MySQLdb
from a_Model import ModelIt

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",
		title = 'Home', user = { 'nickname': 'Miguel' },
		)

@app.route('/db')
def cities_page():
	db = MySQLdb.connect(user="root", host="localhost", db="full_beer_db",  charset='utf8')
#	db = MySQLdb.connect(user="root", host="localhost", db="world_innodb",  charset='utf8')
	with db: 
		cur = db.cursor()
		cur.execute("SELECT Name FROM beer_info LIMIT 15;")
		query_results = cur.fetchall()
	cities = ""
	for result in query_results:
		cities += result[0]
		cities += "<br>"
	return cities

@app.route("/db_fancy")
def cities_page_fancy():
	db = MySQLdb.connect(user="root", host="localhost", db="full_beer_db",  charset='utf8')
	with db:
		cur = db.cursor()
		cur.execute("SELECT name, style, brew FROM beer_info LIMIT 15;")

		query_results = cur.fetchall()
	beer = []
	for result in query_results:
		beer.append(dict(name=result[0], style=result[1], brew=result[2]))
	return render_template('cities.html', cities = beer) 

@app.route('/input')
def cities_input():
	return render_template("input.html")

@app.route('/output')
def cities_output():
	  #pull 'ID' from input field and store it
 	city = request.args.get('ID')
	db = MySQLdb.connect(user="root", host="localhost", db="full_beer_db",  charset='utf8')

 	with db:
 		cur = db.cursor()
    #just select the city from the world_innodb that the user inputs
		cur.execute("SELECT name, style, brew FROM beer_info WHERE Name='%s';" % city)
		query_results = cur.fetchall()

	cities = []
	for result in query_results:
		cities.append(dict(name=result[0], style=result[1], brew=result[2]))
 	#call a function from a_Model package. note we are only pulling one result in the query
	pop_input = cities[0]['brew']
	the_result = ModelIt(city, pop_input)
 	return render_template("output.html", cities = cities, the_result = the_result)	

