from flask import Flask
import logging

def create_app():
    logging.basicConfig(level=logging.DEBUG)

    app = Flask(__name__)

    with app.app_context():
        # Import routes
        from routes import init_app
        init_app(app)
        
    return app

