from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def home():
    return jsonify({'message': 'The flask server is working!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)