from flask import Flask, render_template, request, make_response
import psycopg2, os, jinja2, json

app = Flask(__name__, static_url_path='/static')

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='hawaii',
                            user=os.environ['PGUSER'],
                            password=os.environ['PGPASSWORD'])
    return conn

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/search")
def search():
    place = request.args.get('term')

    conn = get_db_connection()
    cur = conn.cursor()
    place = "{}{}".format(place,'%')
    sql = '''
SELECT 
  concat(name, \' (\', type, \')\') as label, 
  osm_id, 
  name, 
  type, 
  ST_Y(ST_Transform(geometry, 4326)) as lat, 
  ST_X(ST_Transform(geometry, 4326)) as lon F
FROM 
  import.osm_places 
WHERE 
  upper(name) LIKE upper(%s);)
'''
    cur.execute(sql, [place])
    results = []
    for row in cur.fetchall():
        results.append({'label': row[0], 'osm_id': row[1], 'name': row[2], 'type': row[3], 'lat': row[4], 'lon': row[5]})
    cur.close()
    conn.close()
    template = jinja2.Template("""{{ matches | tojson(indent=2) }}""")
    return template.render(matches=results)

@app.route("/find_coffee")
def find_coffee():
    lon = request.args.get('lon')
    lat = request.args.get('lat')

    conn = get_db_connection()
    cur = conn.cursor()
    ewkt = "SRID=4326;POINT("+lon+" "+lat+")"
    print(ewkt)
    sql = '''
SELECT 
  a.geometry <-> ST_Transform(%s::geometry,3857) AS dist, 
  osm_id, 
  name,
  ST_Y(ST_Transform(ST_Centroid(a.geometry), 4326)) AS lat,
  ST_X(ST_Transform(ST_Centroid(a.geometry), 4326)) AS lon
FROM
  import.osm_amenities a
WHERE
  type='cafe'
ORDER BY
  dist
LIMIT 5;
'''
    cur.execute(sql, [ewkt])

    results = []
    for row in cur.fetchall():
        results.append({'dist': row[0], 'osm_id': row[1], 'name': row[2], 'lat': row[3], 'lon': row[4]})
    cur.close()
    conn.close()
    template = jinja2.Template("""{{ matches | tojson(indent=2) }}""")
    return template.render(matches=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0')