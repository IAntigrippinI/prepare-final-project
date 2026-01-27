from connector import ParsingConnector
from database import session_maker
from repository import Repository
from service import ParserService


def fill_db_matches_from_to(from_date: str, to_date: str):
    matches = ParsingConnector("https://api-web.nhle.com/v1").fetch_games_by_date_range(from_date, to_date)
    with session_maker() as session:
        Repository(session).save_games(matches)

        session.commit()


def test():
    matches = ParsingConnector("https://api-web.nhle.com/v1").fetch_games_by_date("2025-09-21")
    print(matches.games)


if __name__ == '__main__':
    fill_db_matches_from_to('2025-09-20', '2025-12-20')
    # test()