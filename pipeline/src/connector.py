from datetime import datetime, timedelta, date

import loguru
import requests

from schemas import TeamStanding, StandingsResponse, SkaterLeadersResponse, SkaterLeader, NHLGame, GameTeam, \
    GamesByDateResponse


class ParsingConnector:

    def __init__(
            self,
            url: str,
    ):
        self._base_url = url


    def fetch_staging(self) -> StandingsResponse:
        staging_url = f"{self._base_url}/standings/now"
        raw = requests.get(staging_url).json()
        teams = []
        for record in raw["standings"]:
            teams.append(
                TeamStanding(
                    team_abbrev=record["teamAbbrev"]["default"],
                    team_name=record["teamName"]["default"],
                    team_common_name=record["teamCommonName"]["default"],
                    place_name=record["placeName"]["default"],
                    team_logo=record["teamLogo"],

                    conference=record["conferenceName"],
                    division=record["divisionName"],

                    games_played=record["gamesPlayed"],
                    wins=record["wins"],
                    losses=record["losses"],
                    ot_losses=record["otLosses"],
                    points=record["points"],
                    point_percentage=record["pointPctg"],

                    goals_for=record["goalFor"],
                    goals_against=record["goalAgainst"],
                    goal_differential=record["goalDifferential"],

                    conference_rank=record["conferenceSequence"],
                    division_rank=record["divisionSequence"],
                    league_rank=record["leagueSequence"],
                    row_date=date.today(),
                )
            )

        return StandingsResponse(
            standings_date_utc=raw["standingsDateTimeUtc"],
            wildcard_indicator=raw["wildCardIndicator"],
            teams=teams,
        )

    def fetch_skater_leaders(self) -> SkaterLeadersResponse:
        leaders_url = f"{self._base_url}/skater-stats-leaders/current"
        raw = requests.get(leaders_url).json()

        leaders = []

        for category_block in raw["categories"]:
            category = category_block["category"]

            for item in category_block["leaders"]:
                leaders.append(
                    SkaterLeader(
                        player_id=item["playerId"],
                        full_name=item["fullName"],
                        team_abbrev=item["teamAbbrev"],
                        position=item["position"],

                        category=category,
                        value=item["value"],
                        games_played=item["gamesPlayed"],
                    )
                )

        return SkaterLeadersResponse(leaders=leaders)

    def fetch_games_by_date(self, date_str: str) -> GamesByDateResponse:
        date_url = f"{self._base_url}/schedule/{date_str}"
        raw = requests.get(date_url).json()

        games: list[NHLGame] = []

        for day in raw.get("gameWeek", []):
            if day.get("date") != date_str:
                continue

            for game in day.get("games", []):
                games.append(
                    NHLGame(
                        game_id=game["id"],
                        # game_state=game["gameState"],
                        # game_type=game["gameType"],
                        game_date=datetime.strptime(date_str, "%Y-%m-%d"),
                        home_name=game["homeTeam"]["abbrev"],
                        away_name=game["awayTeam"]["abbrev"],
                        home_score=game["homeTeam"].get("score", 0),
                        away_score=game["awayTeam"].get("score", 0),
                        # home=GameTeam(
                        #     abbrev=game["homeTeam"]["abbrev"],
                        #     score=game["homeTeam"].get("score"),
                        # ),
                        # away=GameTeam(
                        #     abbrev=game["awayTeam"]["abbrev"],
                        #     score=game["awayTeam"].get("score"),
                        # ),
                    )
                )

        return GamesByDateResponse(date=date_str, games=games)


    def fetch_games_by_date_range(self, start_date_str: str, end_date_str: str) -> list[GamesByDateResponse]:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        date_range = (end_date - start_date).days
        loguru.logger.debug(f"date_range={date_range}")
        fetch_date = start_date
        games = []
        for day in range(date_range):
            date_str = fetch_date.strftime("%Y-%m-%d")
            matches = self.fetch_games_by_date(date_str)
            loguru.logger.debug(f"{date_str } matches={len(matches.games)}")
            games.extend(matches.games)
            fetch_date = fetch_date + timedelta(days=1)
        return games