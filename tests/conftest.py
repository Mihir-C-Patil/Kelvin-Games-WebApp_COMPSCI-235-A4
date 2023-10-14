import pytest
from games import create_app, GameFileCSVReader
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository #, populate
from games.adapters import repository
from pathlib import Path
from games.adapters.repository import AbstractRepository

TEST_DATA_PATH = Path('tests') / 'test_data' / 'games.csv'


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    # populate(TEST_DATA_PATH, repo)
    reader = GameFileCSVReader(TEST_DATA_PATH, repo,
                               False)
    reader.read_csv_file()
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, username='bob', password='jnfdkvn389F'):
        return self.__client.post('/login', data={'username': username,
                                                                 'password': password})

    def logout(self):
        return self.__client.get('authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
