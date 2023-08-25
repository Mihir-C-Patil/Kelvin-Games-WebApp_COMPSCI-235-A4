from games.adapters.repository import AbstractRepository

def get_game(repo: AbstractRepository, id):
    return repo.get_games_by_id(id)

def similar_game(repo: AbstractRepository, genre):
    return repo.get_similar_games(genre)