from flask import Flask, request, jsonify, Response
from models import UserModel
app = Flask(__name__)             

user_model = UserModel()
@app.route("/slack-response", methods=['POST'])
def slack_proxy_response():
    if request.mimetype == 'application/json':
      data = request.get_json()
      user_model.entered_this_round(data["user"]["id"])
      return Response(status=200)
    return Response("Expecting json format not {request.mimetype}", status=400)
if __name__ == "__main__":    
    app.run()