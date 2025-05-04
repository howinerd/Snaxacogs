from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import redis
from rq import Queue

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///snaxa.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure Redis
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        try:
            # Create Redis connection for RQ
            redis_conn = redis.Redis.from_url(
                redis_url,
                ssl=True,
                ssl_cert_reqs="none",
                ssl_check_hostname=False
            )
            
            # Initialize RQ queue
            app.redis_queue = Queue(connection=redis_conn)
            app.config['REDIS_CONNECTED'] = True
            print("Redis connection established successfully")
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            app.config['REDIS_CONNECTED'] = False
    else:
        app.config['REDIS_CONNECTED'] = False
        print("REDIS_URL not found in environment - running without Redis")
    
    # Import and register blueprint from routes __init__.py
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create database tables if they don't exist yet (for SQLite)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    return app