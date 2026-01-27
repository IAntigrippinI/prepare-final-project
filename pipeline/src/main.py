from connector import ParsingConnector
from schemas import GamesByDateResponse
from service import ParserService


def main():
    # con = ParsingConnector("https://api-web.nhle.com/v1")
    # # print(con.fetch_staging())
    # # print(con.fetch_skater_leaders())
    # matchess: GamesByDateResponse = con.fetch_games_by_date("2025-12-18")
    # for match in matchess.games:
    #     print(match)
    service = ParserService()
    service.start_pipline()


if __name__ == "__main__":
    main()