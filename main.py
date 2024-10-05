# uvicorn main:app --reload
from starlette.responses import FileResponse 

from fastapi import FastAPI
from databases import Database
from sqlalchemy import create_engine 

app = FastAPI() 

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/hawaii"

database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)  # Access the DB Engine

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# Add "search" here

# Add "find_coffee" here

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
