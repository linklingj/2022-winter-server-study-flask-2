from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/id/<int:id>', methods=['GET'])
def get(id):
    if id >= 5000 : 
        return {"result" : True}
    else :  
        return {"result" : False}

@app.route('/id', methods=['POST'])
def post():
    res = request.get_json()
    return jsonify({'name' : res['name']})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)