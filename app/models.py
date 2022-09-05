from app import login, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    type = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type',
        'with_polymorphic': '*'
    }

    def __repr__(self):
        return f'User: {self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    residence = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'polymorphic_load': 'inline'
    }

    def __init__(self, residence):
        super().__init__()
        self.residence = residence

    def __repr__(self):
        return f'Admin: {self.residence}'


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    school = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
        'polymorphic_load': 'inline'
    }

    def __init__(self, school):
        super().__init()
        self.school = school

    def __repr__(self):
        return f'Student: {self.school}'


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
        'polymorphic_load': 'inline'
    }

    def __init__(self, course):
        super().__init__()
        self.course = course

    def __repr__(self):
        return f'Teacher: {self.course}'
