from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User
from auth import auth_bp
from views import main_bp

app = Flask(__name__)
app.secret_key = '8217257358'

# DB config - changed to connect to library database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Meral.2010@34.130.33.81:3306/backup'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Setup login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        # Only create the users table
        try:
            db.engine.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL)")
            
            # Create admin user if it doesn't exist
            result = db.engine.execute("SELECT * FROM users WHERE username = 'admin'")
            if not result.fetchone():
                db.engine.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
                print("Admin user created")
            
            print("Database connection successful and users table ready")
        except Exception as e:
            print(f"Error setting up database: {str(e)}")
            print("Please make sure the library database exists and is accessible")
    
    app.run(debug=True)