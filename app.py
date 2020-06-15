from flask import Flask, request
from models import Schema
app = Flask(__name__)             

@app.route("/slack-response", methods=['POST'])                  
def hello():                    
    print(request)
    return "Hello World!"      
if __name__ == "__main__":    
    Schema()
    print("startin app")
    app.run() 