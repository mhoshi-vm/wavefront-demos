from flask import Flask, request
from opentracing.propagation import Format

app = Flask(__name__)

@app.route("/")
def hello():
    print(request)
    print(Format.HTTP_HEADERS)
    print(request.headers)
    hello_to = request.args.get('helloTo')
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
