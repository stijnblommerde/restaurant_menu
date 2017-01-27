# Menu App

**Host**<br />
Udacity

**Course**<br />
Full Stack Foundations

**Exercise**<br />
Final project

**Description**<br />
Menu app created with Flask. Lists out restaurants and allows to view the menu for each restaurant. Users need to authenticate before they can view the data. Administrators are able to edit and delete data as well.

**Required features**
* Implement CRUD operations on a database;
* Use an ORM as an alternative to SQL;
* Use the Flask framework to build a web application;
* Add JSON endpoints.

**Extra features**
* Authentication. Basic authentication with password hashing and tokens;
* Roles and Permissions;
* Users profiles;
* Flash messages.

**Installation**
* add virtual environment: virtualenv -p python3 venv
* install requirements: pip install -r requirements.txt
* create database: python manage.py upgrade
* create roles: python manage.py shell > Role.insert_roles()
* run server: python manage.py runserver
* visit url: localhost:5000
