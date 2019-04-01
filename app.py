import json
import pandas as pd
from flask import Flask, abort, jsonify, request

app = Flask(__name__)
app.debug = True

default_user = [{"user_id": "TaroYamada",
                "password": "PaSSwd4TY",
                "nickname": "たろー",
                "comment": "僕は元気です"}]
user_df = pd.DataFrame(default_user,
                        columns=["user_id", "password", "nickname", "comment"])

print(user_df)

@app.route("//")
def error():
    return jsonify({'error': 'Not found'}), 404

@app.route('/signup', methods=["POST"])
def signup():
    json = request.get_json()
    print(json)

    # user_id, passwordがなかった場合
    try:
        user_id = json['user_id']
    except KeyError as e:
        error = {
                    "message": "Account creation failed",
                    "cause": "required user_id and password"
                }
        return jsonify(error), 400

    try:
        password = json['password']
    except KeyError as e:
        error = {
                    "message": "Account creation failed",
                    "cause": "required user_id and password"
                }
        return jsonify(error), 400

    # user_idが既に存在している場合
    if user_id in list(user_df["user_id"]):
        error = {
                    "message": "Account creation failed",
                    "cause": "already same user_id is used"
                }
        return jsonify(error), 400

    nickname = request.args.get("nickname", default="", type=str)
    comment = request.args.get("comment", default="", type=str)

    print(password)
    print(user_id)
    
    # 成功する場合
    output = {
                "message": "Account successfully created",
                "user": {
                            "user_id": user_id,
                            "nickname": user_id,
                            "comment": comment
                        }
            }

    return jsonify(output), 200

@app.route('/users/{user_id}', methods=["GET"])
def user_info():
    return jsonify(output)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


# おまじない
if __name__ == "__main__":
    app.run(host='0.0.0.0')