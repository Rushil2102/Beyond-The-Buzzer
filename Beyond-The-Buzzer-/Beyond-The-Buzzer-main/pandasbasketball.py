import requests
from bs4 import BeautifulSoup
import PandasBasketball as pb
from PandasBasketball.stats import player_stats, team_stats, player_gamelog, n_days
from PandasBasketball.errors import StatusCode404, TableNonExistent 
import re
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

BASE_URL = "https://www.basketball-reference.com"

def generate_code(player):
    first, last = player.split(" ")
    
    first = first[:2]
    last = last[:5]
    
    return (last + first + "01").lower()


def get_player(player, stat, numeric=False, s_index=False):
    try:
        # Building the URL and making the request
        url = BASE_URL + f"/players/{player[0]}/{player}.html"
        r = requests.get(url)

        # If the page is not found, raise the error
        if r.status_code == 404:
            raise StatusCode404
        else:
            return player_stats(r, stat, numeric=numeric, s_index=s_index)
    except Exception as e:
        logging.error(f"Error in get_player: {str(e)}")
        raise

def get_player_gamelog(player, season, playoffs=False):
    try:
        url = BASE_URL + f"/players/{player[0]}/{player}/gamelog/{season}"
        r = requests.get(url)

        if r.status_code == 404:
            raise StatusCode404
        else:
            return player_gamelog(r, playoffs=playoffs)
    except Exception as e:
        logging.error(f"Error in get_player_gamelog: {str(e)}")
        raise

def get_team(team):
    try:
        url = BASE_URL + f"/teams/{team}"
        r = requests.get(url)

        if r.status_code == 404:
            raise StatusCode404
        else:
            return team_stats(r, team)
    except Exception as e:
        logging.error(f"Error in get_team: {str(e)}")
        raise

def get_n_days(days, player="all"):
    """
    Returns a pandas data frame with all the current 
    season's (avalaible) players ordered by their GmSc 
    over the last n days. Returns a pandas series if a 
    single player is specified
    \tKeyword arguments:
    \t\tdays -- number of days (1-60)
    """
    if days < 1 or days > 60:
        raise TableNonExistent
    else:
        url = BASE_URL + f"/friv/last_n_days.fcgi?n={days}"
        r = requests.get(url)
        return n_days(r, days, player=player)

def get_player_profile(player_code):
    # Construct the URL using the player code
    player_url = f"https://www.basketball-reference.com/players/{player_code[0]}/{player_code}.html"

    response = requests.get(player_url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # Find the <p> elements
        p_elements = soup.find_all("p")

        born_pattern = r'Born:\s*([^,]+),\s*(\d+)'
        height_weight_pattern = r'(\d+\s*cm).*?(\d+\s*kg)'
        nba_debut_pattern = r'NBA Debut:\s*([^<]+)'

        born = ""
        height = ""
        weight = ""
        positions = []
        nba_debut = ""
        experience = ""

        for p in p_elements:
            text = p.get_text()

            # Extract Born information
            match_born = re.search(born_pattern, text, re.I)
            if match_born:
                birthplace = match_born.group(1).strip()
                birthyear = match_born.group(2).strip()
                born = f"Born: {birthplace}, {birthyear}"

            # Extract Height and Weight information
            match_height_weight = re.search(height_weight_pattern, text, re.I)
            if match_height_weight:
                height = match_height_weight.group(1)
                weight = match_height_weight.group(2)

            # Extract Position information
            if "Position:" in text:
                position_text = text.split("Position:")[1].split("Shoots:")[0].strip()
                positions = [position.strip() for position in position_text.split(", and ")]

            # Extract NBA Debut information
            match_nba_debut = re.search(nba_debut_pattern, text, re.I)
            if match_nba_debut:
                nba_debut = match_nba_debut.group(1).strip()



            # If all information is found, exit the loop
            if born and height and weight and positions and nba_debut and experience:
                break

        if not born or not height or not weight or not positions or not nba_debut or not experience:
            return None
        else:
            # Remove spaces after "Positions"
            positions[0] = positions[0].strip()

            player_profile = {
                "Born": born,
                "Height": height,
                "Weight": weight,
                "NBA Debut": nba_debut,
                "Positions": ", ".join(positions)
            }

            return player_profile
    else:
        return None
    
def save_player_data_to_csv(player, stat, filename):
    try:
        player_data = get_player(player, stat)
        with open(filename, 'w') as csv_file:
            # Write the header (column names)
            header = ",".join(player_data.columns)
            csv_file.write(header + "\n")

            # Write the data rows
            for index, row in player_data.iterrows():
                data = ",".join(map(str, row))
                csv_file.write(data + "\n")

        logging.info(f"Player data for {player} saved to {filename}")
    except StatusCode404:
        logging.warning(f"Player data for {player} not found.")

    