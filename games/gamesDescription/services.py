from games.adapters.repository import AbstractRepository

def get_game(repo: AbstractRepository, id):
    return repo.get_games_by_id(id)
