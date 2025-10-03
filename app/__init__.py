from flask import Flask
from flask_socketio import SocketIO
from flask_mail import Mail

socketio = SocketIO()
mail = Mail()

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = "abdulsobur#muhammad"
    app.config.from_pyfile('../config.py')

    # Initialize extensions
    socketio.init_app(app, cors_allowed_origins="*")
    mail.init_app(app)

    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.classroom import classroom_bp
    from .routes.home import home_bp
    from .routes.about import about_bp
    from .routes.student_bio import student_bio_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(classroom_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(student_bio_bp)

    return app
