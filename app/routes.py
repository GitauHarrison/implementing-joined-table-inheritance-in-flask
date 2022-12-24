from app import app, db
from flask import render_template, url_for, redirect, flash, session
from app.forms import LoginForm, RegistrationForm, TeacherForm, StudentForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Student, Teacher


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """index page"""
    users = User.query.all()
    return render_template('index.html', title='Home', users = users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login URL"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Welcome')
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)


@app.route('/register/user/general-info', methods=['GET', 'POST'])
def register_user():
    """Registration URL"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['email'] = form.email.data
        session['identity'] = form.identity.data
        session['password'] = form.password.data
        if session['identity'].lower() == 'teacher':
            flash('Complete your registration as teacher')
            return redirect(url_for('register_teacher'))
        if session['identity'].lower() == 'student':
            flash('Complete your registration as student')
            return redirect(url_for('register_student'))
    return render_template('register.html', title='General User Data', form=form)


@app.route('/register/user/teacher', methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = TeacherForm()
    if form.validate_on_submit():
        teacher = Teacher(
            username = session['username'],
            email = session['email'],
            identity = session['identity'],
            course = form.course.data
        )
        teacher.set_password(session['password'])
        db.session.add(teacher)
        db.session.commit()
        del session['username']
        del session['email']
        del session['identity']
        del session['password']
        flash(f'Registration successful. Login to continue')
        return redirect(url_for('login'))
    return render_template('register_teacher.html', title='Teacher Details', form=form)


@app.route('/register/user/student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            username = session['username'],
            email = session['email'],
            identity = session['identity'],
            age = form.age.data
        )
        student.set_password(session['password'])
        db.session.add(student)
        db.session.commit()
        del session['username']
        del session['email']
        del session['identity']
        del session['password']
        flash(f'Registration successful. Login to continue')
        return redirect(url_for('login'))
    return render_template('register_student.html', title='Student Details', form=form)


@app.route('/logout')
@login_required
def logout():
    """Used to log out a user"""
    logout_user()
    return redirect(url_for('login'))
