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
    return FileResponse('static/index-search-location.html')

@app.get("/search")
async def search(q: str):
    
    # This is the actual query. You may want to work out the SQL statement in a separate `psql` or other database session.
    # The start SQL will give you everything matching `place` exactly which isn't quite what you need. 
    # See the instructions for guidance on how to update this for this jquery autocomplete
    query = '''
SELECT 
  name as label, 
  name
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
        results.append({'label': row[0], 'value': row[1]})
    return results
