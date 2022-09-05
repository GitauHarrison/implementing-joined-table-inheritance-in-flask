from app import app, db
from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import AdminRegistration, StudentRegistration, TeacherRegistration, UserLogin,\
    UserRegistration
from app.models import User, Admin, Teacher, Student
from sqlalchemy.orm import with_polymorphic


def validate_on_submit(self):
    return self.is_submitted() and self.validate()

def is_submitted(self):
    return self.form.is_submitted()

@app.route('/')
@app.route('/account')
@login_required
def account():
    user = db.session.query(User).with_polymorphic([Admin,Student, Teacher])
    if user.type == 'admin':
        return redirect(url_for('admin_account'))
    if user.type == 'student':
        return redirect(url_for('student_account'))
    if user.type == 'teacher':
        return redirect(url_for('teacher_account'))
    return render_template('index.html', title='Admin Account', user=user)


@app.route('/account/admin', methods=['GET', 'POST'])
@login_required
def admin_account():
    if current_user.is_authenticated:
        return redirect(url_for('admin_account'))

    admin = Admin.query.filter_by(username=current_user.username).first()

    studentform = StudentRegistration()
    if studentform.validate_on_submit() and studentform.student.data:
        student = Student(
            username=studentform.username.data,
            email=studentform.email.data,
            school=studentform.school.data)
        student.set_password(studentform.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Student registered!')
        return redirect(url_for('admin_account'))

    teacherform = TeacherRegistration()
    if teacherform.validate_on_submit() and teacherform.teacher.data:
        teacher = Teacher(
            username=teacherform.username.data,
            email=teacherform.email.data,
            course=teacherform.course.data)
        teacher.set_password(teacherform.password.data)
        db.session.add(teacher)
        db.session.commit()
        flash('Teacher registered!')
        return redirect(url_for('admin_account'))

    return render_template(
        'admin.html', title='Admin Account', admin=admin,
        studentform=studentform, teacherform=teacherform)


@app.route('/see/students')
@login_required
def see_students():
    student_query = with_polymorphic(User, Student)
    students = db.session.query(student_query).all()
    return render_template('see_students.html', students=students.items)


@app.route('/see/teachers')
@login_required
def see_teachers():
    teacher_query = with_polymorphic(User, Teacher)
    teachers = db.session.query(teacher_query).all()
    return render_template('see_students.html', teachers=teachers.items)


@app.route('/see/teachers-and-students')
def see_teachers_and_students():
    all_query = with_polymorphic(User, [Teacher, Student])
    teachers_and_students = db.session.query(all_query).all()
    return render_template('see_teachers_and_students.html',
                            teachers_and_students=teachers_and_students.items)


@app.route('/account/student')
@login_required
def student_account():
    student = Student.query.filter_by(username=current_user.username).first()
    return render_template('student.html', title='Student Account', student=student)


@app.route('/account/teacher')
@login_required
def teacher_account():
    teacher = Teacher.query.filter_by(username=current_user.username).first()
    return render_template('teacher.html', title='Teacher Account', teacher=teacher)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        user = db.session.query(User).with_polymorphic([Admin, Student, Teacher])
        if user.type == 'admin':
            return redirect(url_for('admin_account'))
        if user.type == 'student':
            return redirect(url_for('student_account'))
        if user.type == 'teacher':
            return redirect(url_for('teacher_account'))
    form = UserLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        flash('Welcome!')
        return redirect(url_for('admin_account'))
    return render_template('login.html', title='Login', form=form)


# User regitration logic

def user_registration(type):
    form = UserRegistration()
    user = User(username=form.username.data,email=form.email.data,type=type)
    return user


@app.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    if current_user.is_authenticated:
        return redirect(url_for('admin_account'))
    form = AdminRegistration()
    if form.validate_on_submit():
        user = user_registration('admin')
        user.set_password(form.password.data)
        admin = Admin(residence=form.residence.data)
        db.session.add_all([user, admin])
        db.session.commit()
        flash('Admin registered!')
        return redirect(url_for('login'))
    return render_template('admin_register.html', title='Register Admin', form=form)


@app.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('teacher_account'))
    form = TeacherRegistration()
    if form.validate_on_submit():
        teacher = Teacher(
            username=form.username.data,
            email=form.email.data,
            course=form.course.data)
        teacher.set_password(form.password.data)
        db.session.add(teacher)
        db.session.commit()
        flash('Teacher registered!')
        return redirect(url_for('login'))
    return render_template('account.html', title='Account')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
