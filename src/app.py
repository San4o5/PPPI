from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import jwt
import datetime

from users import users
from auth_middleware import require_auth
from role_middleware import check_role

load_dotenv()

app = Flask(__name__)
SECRET = os.getenv("JWT_SECRET")

@app.post("/login")
def login():
    body = request.get_json() or {}
    email = body.get("email")
    password = body.get("password")

    user = next((u for u in users if u["email"] == email and u["password"] == password), None)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    token = jwt.encode({"sub": str(user["id"]), "role": user["role"], "exp": exp}, SECRET, algorithm="HS256")

    return jsonify({
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 900
    })

@app.get("/profile")
@require_auth
def profile():
    return jsonify({
        "user_id": request.user["sub"],
        "role": request.user["role"]
    })

@app.delete("/users/<int:id>")
@require_auth
@check_role(["admin"])
def delete_user(id):
    return jsonify({"message": f"User {id} deleted (demo)"})


if __name__ == "__main__":
    print("SECRET =", SECRET)

    app.run(port=3000, debug=True)
