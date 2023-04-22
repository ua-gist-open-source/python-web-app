# python-flask-app
** Quick start - Initialization **
```
bash populate_database.sh
python3 app.py
```

# Custom Geospatial Web Application With Flask

The objective of this assignment is to build a web application that allows a user to browse a map and search for the closest coffee shops and gas stations. You will use the following technologies:
- Python Flask (web application framework)
- PostGIS (geospatial database)
- Leaflet (javascript library)

## Background
### Python Flask
Flask is a web application framework written in python. It provides an easy and organized way to build dynamic websites. Read the Flask tutorial at https://flask.palletsprojects.com/en/2.2.x/tutorial/ to get a feel for how it works. In this assignment the basic structure of a working Flask application is provided for you so all you need to do is expand in a few places to turn it into a geospatial processing application.

### AJAX and JQuery
In the early days of the web, webpages were generally loaded all at once and rendered one time. This was extremely limiting for interactive applications because every action required loading a whole new page. Javascript provides the interactivity needed to reload parts of the page by changing the document object model or loading content into memory. AJAX (an acronym of the poorly named "Asynchronous JavaScript And XML") allows javascript to send http requests using `XMLHttpRequest` in order to dynamically update an HTML document. There are various ways to use AJAX but the simplest is to use a an AJAX library like JQuery. 

[JQuery](https://jquery.com/) is a javascript library that allows you to update the HTML document based on the results of calls to remote urls. Read https://learn.jquery.com/about-jquery/how-jquery-works/ to understand more about what JQuery is and how it works.

## Assignment

Initially, this repo will have a working Flask application that serves an interactive map.

The first objective for the student will be to add a search feature. This search feature will allow you to enter a place name and it will serarch the PostGIS database for matching results. To accomplish this the student will have to make two things:

- Add a form to the index.html page
- Create a `/search` route in the flask app that searches the database

### Create a /search route in Flask

Add the following `route` to your `app.py`:
```
@app.route("/search")
def search():
    place = request.args.get('place')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT osm_id, name, type, st_asgeojson(st_transform(geometry, 4326)) FROM import.osm_places WHERE upper(name) LIKE upper(%s);', [place])
    places = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('results.html', places=places)

```
In order to use the `psycopg2` library to connect to the postgresql database, add the following to the file at line 2:

```
import psycopg2, os
```
This relies on a function we haven't created yet that actually creates the database connection. Add this above the `route`s:
```
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='hawaii',
                            user=os.environ['PGUSER'],
                            password=os.environ['PGPASSWORD'])
    return conn
```
You should recognize the parameters as those same parameters you used to connect to your `hawaii` database in previous assignments.

