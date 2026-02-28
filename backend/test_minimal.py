from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/test')
def test_api():
    return {'message': 'API test successful'}

if __name__ == '__main__':
    app.run(debug=True)
