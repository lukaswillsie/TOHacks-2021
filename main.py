<<<<<<< HEAD
from flask import Flask, request

app = Flask(__name__)


@app.route("/ping")
def ping():
    return request.args.get("val")


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
=======
from flask import Flask, request

app = Flask(__name__)


@app.route("/ping")
def ping():
    return request.args.get("val")


@app.route('/')
def hello():
    return {'data': 'Hello World!'}, {"Access-Control-Allow-Origin": '*'}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
>>>>>>> e2c8619121723c04358e36195ef3ef15930e1c8e
