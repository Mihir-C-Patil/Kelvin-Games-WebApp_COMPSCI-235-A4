from games.adapters.repository import AbstractRepository


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    games = repo.get_games()
    games_dictionaries = []
    for game in games:
        games_dictionary = {'game_id': game.game_id,
                            'title': game.title,
                            'game_url': game.website_url,
                            'header_image': game.image_url
                            }
        games_dictionaries.append(games_dictionary)
    return games_dictionaries


def get_slide_games(repo: AbstractRepository):
    games = repo.get_games()
    games_dictionaries = []
    i = 0
    for game in games:
        if i < 4:
            games_dict = {'game_id': game.game_id,
                          'title': game.title,
                          'game_url': game.website_url,
                          'header_image': game.image_url
                          }
            games_dictionaries.append(games_dict)
            i += 1
        else:
            break
    return games_dictionaries


def get_games_by_genre(genre, repo: AbstractRepository):
    # Returns games for the specified (target) genre
    games = repo.get_genre_of_games(target_genre=genre)
    games_dicts = []
    for game in games:
        games_dict = {'game_id': game.game_id,
                      'title': game.title,
                      'game_url': game.website_url,
                      'header_image': game.image_url
                      }
        games_dicts.append(games_dict)
    return games_dicts


def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    return [genre.genre_name for genre in genres]
