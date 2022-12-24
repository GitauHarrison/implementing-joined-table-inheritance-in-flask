from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    """Load user by their ID"""
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    """User table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    type = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type'
    }

    def __repr__(self):
        return f'User: {self.username}'

    def set_password(self, password):
        """Hash user password befor storage"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Confirms a user's password"""
        return check_password_hash(self.password_hash, password)

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    age = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
        'polymorphic_load': 'inline'
    }

    def __init__(self, username, email, age):
        super().__init__(username, email, age)
        self.age = age

    def __repr__(self):
        return f'Student: {self.age}'

class Teacher(User):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
        'polymorphic_load': 'inline'
    }

    def __init__(self, username, email, course):
        super().__init__(username, email, course)
        self.course = course

    def __repr__(self):
        return f'Teacher: {self.course}'
