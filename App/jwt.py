from flask_jwt_extended import JWTManager

def setup_jwt(app):
    jwt = JWTManager(app)
    return jwt