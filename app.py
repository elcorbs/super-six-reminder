from flask import Flask, request, jsonify
from models import Schema, UserModel
app = Flask(__name__)             

user_model = UserModel()
@app.route("/slack-response", methods=['POST'])                  
def slack_proxy_response():                    
    print(request)
    if request.data.actions[0].value == "remove_me":
      user_model.entered_this_round(request.data.user.id)
    return "Hello World!"      
if __name__ == "__main__":    
    Schema()
    app.run()