import loguru
from sqlalchemy import insert

from models import GameOrm, TableOrm


class Repository:

    def __init__(self, session):
        self._session = session


    def save_games(self, games):
        loguru.logger.debug(games)
        query = (
            insert(GameOrm).values([g.model_dump() for g in games])
        )
        self._session.execute(query)

    def save_table(self, table):
        query = (
            insert(TableOrm).values([t.model_dump() for t in table])
        )
        self._session.execute(query)
