import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

class Config:
  
   
    SECRET_KEY = os.getenv('SECRET_KEY', '1234erdfch!!ghazswdxt')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URI is not set in the environment variables.")
    
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't', 'y', 'yes']
    
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))  
    REDIS_DB = int(os.getenv('REDIS_DB', 0))  

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400))
    RATE_LIMIT = '5 per minute'

    MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
    MPESA_QLEAP_PAYBILL = os.getenv('MPESA_QLEAP_PAYBILL')
    MPESA_API_KEY = os.getenv('MPESA_API_KEY')

    if not MPESA_SHORTCODE or not MPESA_QLEAP_PAYBILL or not MPESA_API_KEY:
        raise ValueError("MPESA configuration variables are not fully set.")
    

    LOG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.log')

    @staticmethod
    def init_app(app):
        
        file_handler = RotatingFileHandler(Config.LOG_FILE, maxBytes=1000000, backupCount=3)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        
        app.logger.addHandler(file_handler)

        
        app.logger.setLevel(logging.DEBUG)

   
        app.logger.info("App initialized successfully.")
