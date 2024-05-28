# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from myproject import app

# jwt_manager = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, )

