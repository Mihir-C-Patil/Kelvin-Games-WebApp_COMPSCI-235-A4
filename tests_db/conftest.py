import pytest

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from games.adapters import database_repository
from games.adapters.populate_database import GameFileCSVReader
from games.adapters.orm import metadata, map_model_to_tables

TEST_DATA_PATH_FULL = Path('games') / 'adapters' / 'data'
TEST_DATA_PATH_DATABASE_LIMITED = Path('games') / 'tests' / 'test_data'

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///games.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    reader = GameFileCSVReader(TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, database_mode)
    reader.read_csv_file()
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    reader = GameFileCSVReader(TEST_DATA_PATH_FULL, repo_instance, database_mode)
    reader.read_csv_file()
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory
    metadata.drop_all(engine)
