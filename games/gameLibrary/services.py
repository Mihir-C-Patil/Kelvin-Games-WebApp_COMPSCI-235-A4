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
                          'header_image': game.image_url,
                          'price': game.price,
                          'description': game.description
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
                      'header_image': game.image_url,
                      'price': game.price,
                      'description': game.description
                      }
        if games_dict['price'] == 0.0:
            games_dict['price'] = 'Free!'
        games_dicts.append(games_dict)
    return games_dicts


def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    return [genre.genre_name for genre in genres]


def search_games_by_criteria(query: str, criteria: str, repo: AbstractRepository) -> list[dict]:
    search_results = []
    if criteria == "title":
        search_results = repo.search_games_by_title(query)
    elif criteria == "publisher":
        search_results = repo.search_games_by_publisher(query)
    elif criteria == "category":
        search_results = repo.search_games_by_category(query)
    elif criteria == "tags":
        search_results = repo.search_games_by_tags(query)
    games_list = []
    for game in search_results:
        games_dictionary = {'game_id:': game.game_id,
                            'title': game.title,
                            'game_url': game.website_url,
                            'header_image': game.image_url
                            }
        games_list.append(games_dictionary)
    return games_list
