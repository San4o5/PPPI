from flask import request, jsonify
import jwt
import os

def require_auth(f):
    def wrapper(*args, **kwargs):
        print("MIDDLEWARE SECRET =", os.getenv("JWT_SECRET"))  # ← додано

        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing token"}), 401

        token = auth[7:]
        try:
            user = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            request.user = user
        except Exception as e:
            print("JWT ERROR:", e)  # ← ДУЖЕ ВАЖЛИВО!
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper
