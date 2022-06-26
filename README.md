# dealeum
A deal posting web app project for design patterns course


# WINDOWS VSCODE SETUP

0.  Database Configuration
```
Create a database called "dealeum"
```

1. Configure the ***app.config['SQLALCHEMY_DATABASE_URI']*** parameter and set your mysql user id and password
```
BASE CONFIG: 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@localhost:3306/<schema_name>'
```
```
EXAMPLE CONFIG:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:6778@localhost:3306/dealeum'
```


2.  set virtual environment
```
py -m venv env
```
3.  activate the virtual environment
```
.\/env/Scripts/Activate.ps1
```
4.  install required python packages
```
pip install -r requirements.txt
```
5.  set flask app to run the application
```
$env:FLASK_APP = "app"
```
6.  set the environment to development
```
$env:FLASK_ENV = "development"
```
7.  initialize database
```
flask db init
```
8.  migrate database
```
flask db migrate -m "initial migration"
```

9. create the tables
```
flask db upgrade
```

10. run the app
```
flask run
```

11. go to the home url in browser
```
http://127.0.0.1:5000/
```



# Potential Design Patterns
- SQLAlchemy
- Blueprints
- Form Validation
- Template Inheritance
- Message Flashing
- Decorators (role checking, login required etc.)
- DAO (Data access object)
