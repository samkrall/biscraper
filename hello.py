from flask import Flask
app = Flask(__name__)
@app.route("/")
def index():
    return "Testing BiScraper, Datadict.io!"
if __name__ == '__main__':
    app.run(port=5000)