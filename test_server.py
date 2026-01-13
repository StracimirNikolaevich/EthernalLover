"""
Simple test script to verify Flask server can start
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    return "Server is working! Flask is running correctly."

@app.route('/health')
def health():
    return {"status": "ok", "message": "Server is healthy"}

if __name__ == '__main__':
    print("Starting test server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
