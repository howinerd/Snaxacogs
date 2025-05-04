from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Print a message indicating the app is starting
    print("Starting Snaxa Vending application...")
    
    # Run the Flask application
    app.run(debug=True)