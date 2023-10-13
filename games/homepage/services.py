from games.adapters.repository import AbstractRepository


def search_games_by_criteria(query: str, criteria: str,
                             repo: AbstractRepository) -> list[dict]:
    """

    Search games by criteria.

    This method allows you to search for games based on the given criteria
    and query in the repository.

    Parameters:
    query (str): The query string to search for.
    criteria (str): The criteria to use for the search (title, publisher,
    category, tags).
    repo (AbstractRepository): The repository to search in.

    Returns:
    list[dict]: A list of dictionaries representing the search results. Each
    dictionary contains the game id, title, game URL, and header image URL.

    """
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
        games_dictionary = {
                            'game_id': game.game_id,
                            'title': game.title,
                            'game_url': game.website_url,
                            'header_image': game.image_url,
                            'price': game.price,
                            'description': game.description,
                            'release_date': game.release_date
                            }
        games_list.append(games_dictionary)
    return games_list
