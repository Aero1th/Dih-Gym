import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

from routes.auth_routes import auth
from routes.membership_routes import membership
from routes.dashboard_routes import dashboard
from routes.booking_routes import booking
from routes.admin_routes import admin

app = Flask(__name__)

# Use SECRET_KEY from environment when available
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

app.register_blueprint(auth)
app.register_blueprint(membership)
app.register_blueprint(dashboard)
app.register_blueprint(booking)
app.register_blueprint(admin)

if __name__ == '__main__':
    app.run(debug=True)