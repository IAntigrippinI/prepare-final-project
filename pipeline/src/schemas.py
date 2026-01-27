from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel


class TeamStanding(BaseModel):
    team_abbrev: str
    team_name: str
    team_common_name: str
    place_name: str
    team_logo: str

    conference: str
    division: str

    games_played: int
    wins: int
    losses: int
    ot_losses: int
    points: int
    point_percentage: float

    goals_for: int
    goals_against: int
    goal_differential: int

    conference_rank: int
    division_rank: int
    league_rank: int
    row_date: date


class StandingsResponse(BaseModel):
    standings_date_utc: str
    wildcard_indicator: bool
    teams: List[TeamStanding]

### Leaders
class SkaterLeader(BaseModel):
    player_id: int
    full_name: str
    team_abbrev: str
    position: str

    category: str
    value: int
    games_played: int


class SkaterLeadersResponse(BaseModel):
    leaders: List[SkaterLeader]


class GameTeam(BaseModel):
    abbrev: str
    score: Optional[int]


class NHLGameOld(BaseModel):
    game_id: int
    game_state: str
    game_type: int
    start_time_utc: datetime

    home: GameTeam
    away: GameTeam

class NHLGame(BaseModel):
    game_id: int
    # game_state: str
    # game_type: int
    game_date: datetime

    home_name: str
    home_score: Optional[int]
    away_name: str
    away_score: Optional[int]


class GamesByDateResponse(BaseModel):
    date: str
    games: List[NHLGame]