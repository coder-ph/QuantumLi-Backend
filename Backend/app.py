from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from src.startup.database import db
from src.config.config import Config
from src.config.redis_config import init_redis, init_pubsub
from src.startup.routes import register_routes
from src.utils.rate_limiter import limiter
from src.services_layer.auth.token_service import is_token_revoked
from src.utils.logger import logger
from src.error.apiErrors import APIError, NotFoundError, ValidationError, UnauthorizedError, InternalServerError
from src.Models.models import Models
from flask_socketio import SocketIO
from flask_login import LoginManager
import os



app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
app.config.from_object(Config)
socketio = SocketIO(app)
db.init_app(app)
models = Models(db)
models.init_app(app)
jwt = JWTManager(app)
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
 
    try:
        jti = jwt_payload.get("jti", None)
        if not jti:
            logger.warning("JWT payload missing 'jti' — rejecting token by default.")
            return True  
        revoked = is_token_revoked(jti)
        if revoked:
            logger.info(f"Blocked revoked token | jti: {jti}")
        else:
            logger.debug(f"Valid token passed blocklist check | jti: {jti}")
        return revoked

    except Exception as e:
        logger.exception(f"Exception during token blocklist check | Reason: {str(e)}")
        return True 
    
    
CORS(app)
migrate = Migrate(app, db)
limiter.init_app(app)


with app.app_context():
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
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
