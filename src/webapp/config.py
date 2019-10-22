
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'student_db',
    'host': 'localhost',
    'port': 5432,

}
# Create  secrete key so we can use sessions
SECRET_KEY = ')(^s2-dbtv=z9wy%=k6awkh=mr#azaqh98t6z59!t8uxctx8@u'
DEBUG = True
# Create in-memory database
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# Flask-Security features
SECURITY_CHANGEABLE = True
SECURITY_REGISTERABLE = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

# Flask-Security config
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"
