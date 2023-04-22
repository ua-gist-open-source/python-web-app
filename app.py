from flask import Flask, render_template, request
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route("/search")
def search():
    place = request.args.get('place')
    return ("<html><body>Search results for {place}</body></html>".format(place=place))

if __name__ == "__main__":
    app.run(host='0.0.0.0')