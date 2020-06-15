from flask import Flask, request, jsonify, Response
from models import UserModel
import json
app = Flask(__name__)             

user_model = UserModel()
@app.route("/slack-response", methods=['POST'])
def slack_proxy_response():
    print(request.form.get('payload'))
    data = json.loads(request.form.get('payload'))
    print(data)
    user_model.entered_this_round(data["user"]["id"])
    return Response(status=200)
if __name__ == "__main__":    
    app.run()