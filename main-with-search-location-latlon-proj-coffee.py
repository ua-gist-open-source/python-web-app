# uvicorn main:app --reload
from starlette.responses import FileResponse 

from fastapi import FastAPI
from databases import Database
from sqlalchemy import create_engine 

app = FastAPI() 

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/hawaii"

database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)  # Access the DB Engine 

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_index():
    # return FileResponse('static/index.html')
    return FileResponse('static/index-search-location-latlon-coffee.html')

@app.get("/search")
async def search(q: str):
    
    # This is the actual query. You may want to work out the SQL statement in a separate `psql` or other database session.
    # The start SQL will give you everything matching `place` exactly which isn't quite what you need. 
    # See the instructions for guidance on how to update this for this jquery autocomplete
    query = '''
SELECT 
  name as label, 
  name,
  ST_X(ST_Transform(geometry, 4326)) as lon,
  ST_Y(ST_Transform(geometry, 4326)) as lat
FROM 
  import.osm_places 
WHERE 
  upper(name) like :name
'''
    rows = await database.fetch_all(query=query, values={"name": "%{}%".format(q.upper())})
    # For our pursposes we want to save the results in a special json format with two keys: `label` and `value`.
    # That's because jquery `autocomplete` will work if follow this format convention for our JSON output.
    
    results = []
    for row in rows:
        results.append({'label': row[0], 'value': row[1], 'lon': row[2], 'lat': row[3]})
    return results


@app.get("/find_coffee")
async def find_coffee(lon: str, lat: str):
    query = '''
SELECT 
  a.geometry <-> ST_Transform(ST_SetSRID(ST_Point({},{}),4326),3857) AS dist, 
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
'''.format(lon, lat)
    print(query)
    
    rows = await database.fetch_all(query=query)

    results = []
    for row in rows:
        results.append({'dist': row[0], 'osm_id': row[1], 'name': row[2], 'lat': row[3], 'lon': row[4]})
    # template = jinja2.Template("""{{ matches | tojson(indent=2) }}""")
    # return template.render(matches=results)
    return results