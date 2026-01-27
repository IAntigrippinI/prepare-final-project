from sqlalchemy import Column, Integer, DateTime, String, Float, Date

from database import Base


class GameOrm(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    game_date = Column(DateTime)
    home_name = Column(String)
    home_score = Column(Integer)
    away_name = Column(String)
    away_score = Column(Integer)

class TableOrm(Base):
    __tablename__ = "table"
    id = Column(Integer, primary_key=True)
    row_date = Column(Date)
    team_abbrev = Column(String)
    team_name = Column(String)
    team_common_name = Column(String)
    place_name = Column(String)
    team_logo = Column(String)
    conference = Column(String)
    division = Column(String)
    games_played = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    ot_losses = Column(Integer)
    points = Column(Integer)
    point_percentage = Column(Float)
    goals_for = Column(Integer)
    goals_against = Column(Integer)
    goal_differential = Column(Integer)
    conference_rank = Column(Integer)
    division_rank = Column(Integer)
    league_rank = Column(Integer)