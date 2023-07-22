from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user"""

        hashed = bcrypt.generate_password_hash(password)
        # Turn bytestring into normal(unicode utf8) string

        hashed_utf8 = hashed.decode("utf8")

        # return instance of user info and hashed password
        return cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

    @classmethod
    def authenticate(cls, username, password):
        """
        Validate that user exists & password is correct

        Return user if valid; else return Flase

        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.Text, db.ForeignKey("users.username"))
