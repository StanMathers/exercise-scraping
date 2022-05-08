from classes.requesthandling import RequestToSteam
from classes.parsinghandling import SteamParsing


def main():
    req = RequestToSteam(count=100)
    parsing = SteamParsing(req.html_from_json())
    print(parsing.to_dataframe())


if __name__ == '__main__':
    main()