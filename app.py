from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from .Backend.src.startup.database import db
from .Backend.src.config.config import Config
from .Backend.src.config.redis_config import init_redis, init_pubsub
from .Backend.src.startup.routes import register_routes
from .Backend.src.error.apiErrors import APIError, NotFoundError, ValidationError, UnauthorizedError, InternalServerError

app = Flask(__name__)


app.config.from_object(Config)


db.init_app(app)
jwt = JWTManager(app)
CORS(app)
migrate = Migrate(app, db)

redis_client = init_redis()
pubsub = init_pubsub()


register_routes(app)


@app.errorhandler(APIError)
def handle_api_error(error):
    
    response = {
        'message': error.message,
        'error_code': error.error_code
    }
    return jsonify(response), error.status_code

@app.errorhandler(500)
def handle_internal_server_error(error):
    
    app.logger.error(f"Internal Server Error: {str(error)}")
    return jsonify({"message": "An unexpected error occurred. Please try again later."}), 500


@app.route('/')
def home():
    return "Welcome to the logistics platform backend!"

if __name__ == '__main__':
    app.run(debug=True)
