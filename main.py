<<<<<<< HEAD
from flask import Flask, request

app = Flask(__name__)

BASE_HEADERS = {"Access-Control-Allow-Origin": '*'}


@app.route("/ping/<text>")
def ping(text):
    return {"result": text.upper()}, BASE_HEADERS


@app.route('/')
def hello():
    return {'data': 'Hello World!'}, BASE_HEADERS


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
=======
from flask import Flask, request
from peacock import main

app = Flask(__name__)

BASE_HEADERS = {"Access-Control-Allow-Origin": '*'}


@app.route("/ping")
def ping():
    text = request.args.get("text")
    return {"result": main(text)}, BASE_HEADERS


@app.route('/')
def hello():
    return {'data': 'Hello World!'}, BASE_HEADERS


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
>>>>>>> 3025880aa39d2a2957383760a1e46f609a24bff1
