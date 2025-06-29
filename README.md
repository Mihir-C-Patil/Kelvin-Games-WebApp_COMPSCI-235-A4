# Kelvin Games WebApp Repository

Welcome to the Kelvin Games WebApp repository! This repository contains the implementation of the web application for the Kelvin Games platform, as part of the CompSci 235 course in Semester 2, 2023.

## Description

This repository is dedicated to the development of the Kelvin Games web application. It encompasses a Flask-based application that showcases an interactive gaming platform. The application is designed to display game-related information fetched from our domain model. You can choose to either use the provided domain model or your own implementation from CodeRunner assignment 1.


## Prerequisites
You must have Python 3.11 installed!

## Installation

**Installation via requirements.txt**

**Windows**
```shell
$ cd <project directory>
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**
```shell
$ cd <project directory>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File or PyCharm'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add Interpreter'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *project directory*, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Testing
Before testing, you must go into ```games/__init__.py```.
Then, on line 16, change ```def create_app(test_config=None):``` to ```def create_app(test_config=True):```.

Then, in the terminal (root directory) run:
```shell
$ python -m pytest
```

If you only wish to test the database components, in the terminal (root directory), run:
```shell
$ python -m pytest -v tests_db
```

## Configuration

The *project directory/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

These settings are for the database version of the code:

* `SQLALCHEMY_DATABASE_URI`: The URI of the SQlite database, by default it will be created in the root directory of the project.
* `SQLALCHEMY_ECHO`: If this flag is set to True, SQLAlchemy will print the SQL statements it uses internally to interact with the tables.


## Repository Mode
In the *games/.env* file, the REPOSITORY flag value can be changed to select the repository mode.

* `REPOSITORY`: This flag allows us to easily switch between using the Memory repository or the SQLAlchemyDatabase repository. Can be set to either 'DATABASE' of SqlAlchemy or 'MEMORY' for memory database.
 
## Data sources

The data files are modified excerpts downloaded from:

https://huggingface.co/datasets/FronkonGames/steam-games-dataset
