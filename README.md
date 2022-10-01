# How Do You Implement Joined Table Inheritance in Flask?

Joined table inheritance in SQLAlchemy relies on two core concepts of object-oriented programming (OOP):

- Inheritance
- Polymorphism

If they are unfamiliar to you, I will briefly explain them below. Remember, to work with Python following OOP, you will need basic understinding of classes, objects and the other OOP concepts such as Encapsulation and Abstraction. So, be sure to study these. But first, an overview of what to expect in this project.

1. [About the application](#about-the-application)
2. [Inheritance](#inheritance)
3. [Polymorphism](#polymorphism)
4. [Joined Table Inheritance in SQLAlchemy](#joined-table-inheritance-in-sqlalchemy)
5. [Define Your Model Using the SQLAlchemy ORM](#define-your-model-using-the-sqlalchemy-orm)
6. [Update Your Models](#update-your-models)

## Note

>At this point in my understanding of joined table inheritance, I am of the belief that it is only theoretically possible to use it. It is nearly impractical to implement this database design model when building web applications. [See how I came to this conclusion](https://github.com/GitauHarrison/user-roles-in-flask/blob/main/README.md#background).

## About the Application
### Technologies Used

- Flask and Python
- Flask Migrate and Flask SQLAlchemy for database management
- More in [requirements.txt](requirements.txt) file

### Contributors

[![GitHub Contributors](https://img.shields.io/github/contributors/GitauHarrison/implementing-joined-table-inheritance-in-flask)](https://github.com/GitauHarrison/implementing-joined-table-inheritance-in-flask/graphs/contributors)


### License

- [x] [MIT](LICENCE) license


### Testing the Application Locally

* Clone this repo:
  ```python
  $ git clone git@github.com:GitauHarrison/implementing-joined-table-inheritance-in-flask.git
  ```

* Move into the cloned directory:

  ```python
  $ cd implementing-joined-table-inheritance-in-flask
  ```

* Create and activate your virtual environment:

  ```python
  $ mkvirtualenv venv # I am using virtualenvwrapper
  ```

* Install project dependencies within your active virtual environment:

  ```python
  (venv)$ pip3 install -r requirements.txt
  ```

* Environment variables:
    * Create a file called `.env` in the root directory of the project
      ```python
      (venv)$ touch .env
      ```
    * Add the following line to the file as seen in `.env-template`:
      ```python
      SECRET_KEY=
      ```

* Start the flask server:

  ```python
  (venv)$ flask run
  ```

* Access the application on http://127.0.0.1:5000/

## Inheritance

This concept allows a child class to acquire the features of a parent class. The child class will be defined with new or modified attributes or non at all. In other words, the child class will be extended by the parent class. The child class is sometimes referred to as the "derived" class or the "subclass". The parent class is sometimes referred to as the "base" class.

```python
class Parent():
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'Parent: {self.username}'


class Child(Parent):
    pass
```

We have defined two classes: `Parent` and `Child`. The `Parent` class has the attributes `username` and `email`. This class is passed as a parameter in the `Child` class which, at the moment, has no attributes.

To test our work, let us run these in an active Python interpreter:

```python
$ python3

>>> parent = Parent('harry', 'harry@email.com')
>>> parent
# Output
Parent: harry

>>> parent.username, parent.email
# Output
('harry', 'harry@email.com')

>>> child = Child('muthoni', 'muthoni@email.com')
>>> child
# Output
Parent: muthoni

>>> child.username
# Output
'muthoni'
```

`parent` and `child` are objects of their respective classes. Instantiating these objects give data relevant to them. Notice that when you call the `child` object the output is "Parent: muthoni". This is because the child has inherited the in-built `__repr__()` function from the parent which has the string "Parent".

## Polymorphism

Polymorphism is the ability to take many(poly) forms(morphism). Polymorphism in Python allows us to define methods that do not exist in the parent class or modify these methods if they exist in the parent class.

```python
class Parent():
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'Parent: {self.username}'


class Child(Parent):
    def __init__(self, username, email, age):
        super().__init__(username, email)
        self.age = age

    def __repr__(self):
        return f'Child: {self.username}, {self.age}''
```

We have modified the `__repr__()` function for the `Child` class to have its own string besides the dynamic `username` and `email` values. The `Child` class has an additional `age` attribute that does not exist in the parent.

```python
$ python

>>> parent = Parent('harry', 'harry@email.com')
# Output
Parent: harry

>>> child = Child('muthoni', 'muthoni@email.com', 3)
# Output
Child: muthoni, 3
```

Notice that the parent's `__repr__()` function has been overriden by the child's. This is because the child defined its own `__repr__()` function. Additionally, the `age ` attribute is only present in the child class.


## Joined Table Inheritance in SQLAlchemy

There is an exhaustive [article](https://github.com/GitauHarrison/notes/blob/master/databases/joined_table_inheritance.md) on this concept that I recommend you check it out if you want to learn what joined table inheritance is. Below, I will show you how to structure your flask application to accommodate this concept.

## Define Your Model Using the SQLAlchemy ORM

ORMs allow applications to manage a database using high-level entities such as classes, objects and methods instead of tables and SQL. The job of the ORM is to translate the high-level operations into database commands. A flask-friendly wrapper to the [SQLAlchemy](http://www.sqlalchemy.org/) package is the [Flask-SQLAlchemy](http://packages.python.org/Flask-SQLAlchemy).

See [models.py](/app/models.py) for reference.

These tables were created by running the commands shown below. You do not have to run them if you have cloned this repository:

```python
(venv)$ flask db init
(venv)$ flask db migrate
(venv)$ flask db upgrade
```

## Update Your Models

Head over to the _registration_ page to create a new admin user.

![Admin registration page]()

The route handling this action has:

```python
# Update admin table
```

You will be redirected to the _login_ page after submitting the data.

![User login page]()

Notice that the `login()` view function uses the class `User` for all the available users of the application.

```python
# Login view function
```

You should be redirected to the relevant page. In my case, since I am logging in as an admin user, I will go to the admin dashboard.

![Admin dashboard]()

Querrying the database using joined table inheritance is also supported.

```python
# Query db for all students
```

When I click the _see all students_ link, I get a list of all available students registered in the database.

![See all registered students]()

