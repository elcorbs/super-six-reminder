from flask import Flask, request, jsonify
from models import Schema
app = Flask(__name__)             

@app.route("/slack-response", methods=['POST'])                  
def hello():                    
    print(jsonify(request))
    return "Hello World!"      
if __name__ == "__main__":    
    Schema()
    app.run() 