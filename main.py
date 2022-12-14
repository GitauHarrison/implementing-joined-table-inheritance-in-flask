from app import app, db
from app.models import User, Student, Teacher


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Teacher=Teacher, Student=Student)
