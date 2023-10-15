from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Config class for managing application configuration.

    Attributes:
        FLASK_APP (str): The name of the Flask application.
        FLASK_ENV (str): The environment mode of the Flask application.
        SECRET_KEY (str): The secret key used for encryption and session
        management.
        TESTING (str): The testing mode of the application.
        REPOSITORY (str): The repository used for database operations.
        SQLALCHEMY_DATABASE_URI (str): The URI for connecting to the database.
        SQLALCHEMY_ECHO (bool): Indicates whether SQL queries should be echoed.

    Note:
        This class relies on environment variables being set using the
        `environ` module from the `os` package, and the `dotenv` package
        for loading environment variables from the `.env` file.


        The values of the attributes are obtained from the corresponding
        environment variables.

    """
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    TESTING = environ.get('TESTING')
    REPOSITORY = environ.get('REPOSITORY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    echo_string = environ.get('SQLALCHEMY_ECHO')
    SQLALCHEMY_ECHO = False
    if echo_string.lower().strip() == 'true':
        SQLALCHEMY_ECHO = True
