from flask import Flask, request, jsonify, Response
from models import Schema, UserModel
app = Flask(__name__)             

user_model = UserModel()
@app.route("/slack-response", methods=['POST'])
def slack_proxy_response():
    if request.mimetype == 'application/json':
      data = request.get_json()
      print(data)
      if data["actions"][0]["value"] == "remove_me":
        user_model.entered_this_round(data["user"]["id"])
    return Response(status=200)
if __name__ == "__main__":    
    Schema()
    app.run()