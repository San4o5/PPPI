from flask import request, jsonify

def check_role(roles):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if request.user.get("role") not in roles:
                return jsonify({"error": "Forbidden"}), 403
            return f(*args, **kwargs)

        wrapper.__name__ = f.__name__
        return wrapper
    return decorator
