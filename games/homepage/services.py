from games.adapters.repository import AbstractRepository


def search_games_by_criteria(query: str, criteria: str,
                             repo: AbstractRepository) -> list[dict]:
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
