from flask import Flask, render_template, request
import psycopg2, os

app = Flask(__name__, static_url_path='/static')

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='hawaii',
                            user=os.environ['PGUSER'],
                            password=os.environ['PGPASSWORD'])
    return conn

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route("/search")
def search():
    place = request.args.get('place')
    # place_like = "%{}%".format(place)
    # return ("<html><body>Search results for {place}</body></html>".format(place=place))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT osm_id, name, type, st_asgeojson(geometry) FROM import.osm_places WHERE upper(name) LIKE upper(%s);', [place])
    places = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('results.html', places=places)


@app.route('/searcg')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM places WHERE ;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)

if __name__ == "__main__":
    app.run(host='0.0.0.0')