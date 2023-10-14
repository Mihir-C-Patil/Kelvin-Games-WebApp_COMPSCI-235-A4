from sqlalchemy import select, inspect
from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    # Test to check table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game', 'game_genres', 'genre', 'publisher', 'review', 'user', 'wishlist', 'wishlist_games']

def test_database_populate_select_all_games(database_engine):
    # Test to check games
    inspector = inspect(database_engine)
    name_of_games_tables = inspector.get_table_names()[0]
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_games_tables]])
        result = connection.execute(select_statement)
        all_games = []
        for row in result:
            all_games.append((row['id'], row['game_title']))
        num_games = len(all_games)
        assert num_games == 14
        assert all_games[0] == (7940, 'Call of Duty® 4: Modern Warfare®')
        assert all_games[13] == (1998840, 'Arcadia')

def test_database_populate_select_all_publishers(database_engine):
    # Test to check publishers
    inspector = inspect(database_engine)
    name_of_publisher_tables = inspector.get_table_names()[3]
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_publisher_tables]])
        result = connection.execute(select_statement)
        all_publishers = []
        for row in result:
            all_publishers.append((row['publisher_name']))
        assert len(all_publishers) == 14

def test_database_populate_select_all_genres(database_engine):
    # Test to check genres
    inspector = inspect(database_engine)
    name_of_genre_table = inspector.get_table_names()[2]
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_genre_table]])
        result = connection.execute(select_statement)
        all_genres = []
        for row in result:
            all_genres.append(row['genre_name'])
        assert len(all_genres) == 1
        assert all_genres[0] == 'Action'

def test_database_populate_select_all_genres_association(database_engine):
    # Test to check genres association table
    inspector = inspect(database_engine)
    name_of_genre_table = inspector.get_table_names()[1]
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_genre_table]])
        result = connection.execute(select_statement)
        all_genres = []
        for row in result:
            all_genres.append((row['game_id'], row['genre_name']))
        assert all_genres[0] == (7940, 'Action')

