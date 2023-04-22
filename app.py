from flask import Flask, render_template
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route("/search")
def search():
    return ("<html><body>Search results</body></html>")

if __name__ == "__main__":
    app.run(host='0.0.0.0')