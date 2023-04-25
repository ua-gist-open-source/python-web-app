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

if __name__ == "__main__":
    app.run(host='0.0.0.0')