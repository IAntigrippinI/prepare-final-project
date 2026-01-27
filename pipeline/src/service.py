from datetime import date

import loguru

from connector import ParsingConnector
from database import session_maker
from repository import Repository


class ParserService:


    def __init__(self):
        self._connector = ParsingConnector("https://api-web.nhle.com/v1")
        self._repository = Repository


    def start_pipline(self):
        today = date.today().strftime("%Y-%m-%d")
        games = self._connector.fetch_games_by_date(today)
        loguru.logger.info(f"Fetch: {len(games.games)} games")
        table = self._connector.fetch_staging()
        with session_maker() as session:
            self._repository(session).save_games(games.games)
            self._repository(session).save_table(table.teams)

            session.commit()