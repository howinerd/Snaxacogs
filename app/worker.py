import os
import redis
from rq import Worker, Queue
from dotenv import load_dotenv
from app import create_app
import time
import urllib.parse
import ssl

# Load environment variables from .env file
load_dotenv()

# Create a Flask application context
app = create_app()
app.app_context().push()

def start_worker():
    # Get Redis connection from environment variable
    redis_url = os.getenv('REDIS_URL')

    if not redis_url:
        print("ERROR: REDIS_URL environment variable is not set!")
        print("Running in development mode without background processing...")
        return False

    print(f"Connecting to Redis at: {redis_url.split('@')[1] if '@' in redis_url else 'endpoint hidden'}")

    try:
        # Parse the URL to construct connection with correct SSL settings
        parsed_url = urllib.parse.urlparse(redis_url)
        
        # Create SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        conn = redis.Redis(
            host=parsed_url.hostname,
            port=parsed_url.port,
            username=parsed_url.username,
            password=parsed_url.password,
            ssl=True,
            ssl_cert_reqs="none",
            ssl_check_hostname=False
        )
        
        # Test the connection
        conn.ping()
        print("Successfully connected to Redis!")
        
        # Create a queue
        q = Queue(connection=conn)
        
        # Create a worker
        worker = Worker([q], connection=conn)
        
        # Start the worker
        print("Starting worker...")
        worker.work()
        return True
    except Exception as e:
        print(f"Error connecting to Redis: {str(e)}")
        print("Running in development mode without background processing...")
        return False

if __name__ == '__main__':
    success = start_worker()
    
    if not success:
        print("Worker is running in development mode (no Redis).")
        print("Background tasks will not be processed.")
        
        # Keep the script running so the batch file doesn't close
        while True:
            print(".", end="")
            time.sleep(10)