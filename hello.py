from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "<H1> Testing BiScraper, Datadict.io! <H1>"

@app.route('/about')
def about():
    return "<H1> About Datadict.IO <H1>"

if __name__ == '__main__':
    app.run(debug=True)