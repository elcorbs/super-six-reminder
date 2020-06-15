from flask import Flask, request, jsonify, Response
from models import Schema, UserModel
app = Flask(__name__)             

user_model = UserModel()
@app.route("/slack-response", methods=['POST'])                  
def slack_proxy_response():
    request_json = request.get_json()
    print(request_json)
    if request_json["actions"][0]["value"] == "remove_me":
      user_model.entered_this_round(request_json["user"]["id"])
    return Response(status=200)
if __name__ == "__main__":    
    Schema()
    app.run()