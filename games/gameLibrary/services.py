from games.adapters.repository import AbstractRepository


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    games = repo.get_games()
    games_dicts = []
    for game in games:
        games_dict = {'game_id': game.game_id,
                      'title': game.title,
                      'game_url': game.website_url,
                      'header_image': game.image_url
                      }
        games_dicts.append(games_dict)
    return games_dicts
