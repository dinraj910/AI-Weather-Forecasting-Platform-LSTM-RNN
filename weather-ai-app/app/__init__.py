
from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Services (Optional: Lazy load in routes/services)
    # from app.services.preprocessing_service import PreprocessingService
    # PreprocessingService.get_instance()

    # Register Blueprints
    from app.routes.main_routes import main_bp
    from app.routes.api_routes import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
