import pandas as pd
from bs4 import BeautifulSoup, NavigableString
import pandasbasketball as pb
import logging

# Initialize the logger
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

from PandasBasketball.errors import TableNonExistent

def player_stats(request, stat, numeric=False, s_index=False):
    try:
        supported_tables = ["totals", "per_minute", "per_poss", "advanced",
                            "playoffs_per_game", "playoffs_totals", "playoffs_per_minute",
                            "playoffs_per_poss", "playoffs_advanced"]

        if stat == "per_game":
            soup = BeautifulSoup(request.text, "html.parser")
            table = soup.find("table", id="per_game")
        elif stat in supported_tables:
            soup = BeautifulSoup(request.text, "html.parser")
            comment_table = soup.find(text=lambda x: isinstance(x, NavigableString) and stat in x)
            soup = BeautifulSoup(comment_table, "html.parser")
            table = soup.find("table", id=stat)
        else:
            raise TableNonExistent

        # Get the whole data frame
        df = get_data_master(table, "player")

        if stat == "per_poss" or stat == "playoffs_per_poss":
            del df[None]
        elif stat == "advanced" or stat == "playoffs_advanced":
            del df["\xa0"]

        if numeric:
            df[df.columns] = df[df.columns].apply(pd.to_numeric, errors="ignore")
        if s_index:
            df.set_index("Season", inplace=True)

        return df
    except Exception as e:
        logging.error(f"Error in player_stats: {str(e)}")
        raise

def player_gamelog(request, playoffs=False):
    try:
        if playoffs:
            soup = BeautifulSoup(request.text, "html.parser")
            comment_table = soup.find(text=lambda x: isinstance(x, NavigableString) and "pgl_basic_playoffs" in x)
            soup = BeautifulSoup(comment_table, "html.parser")
            table = soup.find("table", id="pgl_basic_playoffs")
        else:
            soup = BeautifulSoup(request.text, "html.parser")
            table = soup.find("table", class_="row_summable sortable stats_table")

        df = get_data_master(table, "gamelog")
        df.set_index("Rk", inplace=True)

        return df
    except Exception as e:
        logging.error(f"Error in player_gamelog: {str(e)}")
        raise

def team_stats(request, team):
    try:
        soup = BeautifulSoup(request.text, "html.parser")
        table = soup.find("table", id=team)

        df = get_data_master(table, "team")
        del df["\xa0"]

        return df
    except Exception as e:
        logging.error(f"Error in team_stats: {str(e)}")
        raise

def n_days(request, days, player):
    try:
        soup = BeautifulSoup(request.text, "html.parser")
        table = table = soup.find("table", id="players")

        if table is not None:
            df = get_data_master(table, "n_days")
            df.set_index("Player", inplace=True)

            if player == "all":
                return df
            else:
                return df.loc[player]
        else:
            raise TableNonExistent
    except Exception as e:
        logging.error(f"Error in n_days: {str(e)}")
        raise

def get_data_master(table, tdata):
    try:
        columns = []

        # Check if the table is None and log a debug message
        if table is None:
            logging.debug(f"Table not found for data: {tdata}")
            return None

        heading = table.find("thead")
        if heading is None:
            logging.debug(f"<thead> element not found in the table for data: {tdata}")
            return None  # Handle the case where the table doesn't have a <thead> element

        heading_row = heading.find("tr")
        for x in heading_row.find_all("th"):
            columns.append(x.string)

        body = table.find("tbody")
        if body is None:
            logging.debug(f"<tbody> element not found in the table for data: {tdata}")
            return None  # Handle the case where the table doesn't have a <tbody> element

        rows = body.find_all("tr")

        data = []
        for row in rows:
            temp = []
            th = row.find("th")
            td = row.find_all("td")
            if th:
                temp.append(th.text)
            else:
                continue

            if tdata == "gamelog" or tdata == "n_days":
                for v in td:
                    if v.text == "Inactive" or v.text == "Did Not Play" or v.text == "Did Not Dress":
                        temp.extend([""] * (len(columns) - 8))  # 8 is the min. number of columns all tables have
                        break
                    else:
                        temp.append(v.text)
                data.append(temp)
            elif tdata == "player" or tdata == "team":
                for v in td:
                    temp.append(v.text)
                data.append(temp)

        # Removes the table's mid headers
        if tdata == "gamelog" or tdata == "n_days":
            data = [l for l in data if len(l) == len(columns)]

        df = pd.DataFrame(data)
        df.columns = columns

        return df
    except Exception as e:
        logging.error(f"Error in get_data_master: {str(e)}")
        raise

user_input = "victor wembanyama"
player_code = pb.generate_code(user_input)
logging.info(f"Player code generated: {player_code}")
url = f"https://www.basketball-reference.com/players/c/{player_code}.html"
df = pb.get_player(player_code, "per_game")
logging.info(f"Player stats retrieved:\n{df}")
for column in df.columns:
    logging.info(f"Column: {column}")
