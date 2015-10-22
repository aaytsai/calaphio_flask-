# Flask Config Vars
DEBUG = True
TESTING = True
SECRET_KEY = "This is a secret"
SESSION_COOKIE_NAME = "calaphio_flask"
SERVER_NAME = "localhost:5000"

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI='mysql+mysqldb://website@localhost/website'
SQLALCHEMY_ECHO=False

# Flask-Login
LOGIN_DISABLED = False