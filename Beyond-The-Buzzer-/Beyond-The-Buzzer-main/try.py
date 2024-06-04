from flask import Flask, render_template, request
import pandasbasketball as pb
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import logging

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

@app.route("/", methods=["GET", "POST"])
def index():
    player_name = None
    player_code = None
    player_url = None
    image_url = None
    player_data = None
    chart_base64 = None
    player_data_1 = None
    player_data_2 = None
    player_data_3 = None
    player_data_4 = None
    player_data_5 = None
    chart_base64_points = None
    chart_base64_assists = None
    chart_base64_blocks = None
    chart_base64_rebounds = None
    chart_base64_steals = None
    chart_base64_turnovers = None
    chart_base64_stacked = None
    shooting_data = None
    n_days_data = None
    player_profile = None

    if request.method == "POST":
        
        player_name = request.form["player_name"]
        player_code = pb.generate_code(player_name)
        player_url = f"https://www.basketball-reference.com/players/c/{player_code}.html"
        image_url = f"https://www.basketball-reference.com/req/202106291/images/headshots/{player_code}.jpg"

        pb.save_player_data_to_csv(player_code, "per_game", "per_game_data.csv")
        pb.save_player_data_to_csv(player_code, "per_minute", "per_minute_data.csv")
        pb.save_player_data_to_csv(player_code, "per_poss", "per_poss_data.csv")
        pb.save_player_data_to_csv(player_code, "playoffs_per_minute", "playoffs_per_minute_data.csv")
        pb.save_player_data_to_csv(player_code, "playoffs_per_poss", "playoffs_per_poss_data.csv")


        player_data_1 = pb.get_player(player_code, "per_game")
        player_data_2 = pb.get_player(player_code, "per_minute")
        player_data_3 = pb.get_player(player_code, "per_poss")
        player_data_4 = pb.get_player(player_code, "playoffs_per_minute")
        player_data_5 = pb.get_player(player_code, "playoffs_per_poss")
        shooting_data = player_data_1[["Season","2P","3P","FT","PTS"]]
        # player_profile = pb.get_player_profile(player_code)
        logging.info(f"Data retrieved for player: {player_name}, code: {player_code}")


        
        
        
            
 # ... (other imports and code) ...
 

        if player_data_1 is not None:
            seasons = player_data_1["Season"]
            points = player_data_1["PTS"].astype(float)
            assists = player_data_1["AST"].astype(float)
            blocks = player_data_1["BLK"].astype(float)
            rebounds = player_data_1["TRB"].astype(float)
            steals = player_data_1["STL"].astype(float)
            turnovers = player_data_1["TOV"].astype(float)
            points_2P = shooting_data["2P"].astype(float)
            points_3P = shooting_data["3P"].astype(float)
            points_FT = shooting_data["FT"].astype(float)
            total_points = points_FT + points_2P * 2 + points_3P * 3

            logging.info("Data processed successfully.")

            # Create the Points per Season chart
            plt.figure(figsize=(10, 6))
            plt.bar(seasons, points, color='royalblue')
            plt.title(f"Points per Season for {player_name}")
            plt.xlabel("Season")
            plt.ylabel("Points")
            plt.xticks(rotation=45, fontsize=10)

            # Save the Points chart to a BytesIO buffer and encode it as a base64 image
            chart_buffer_points = BytesIO()
            plt.savefig(chart_buffer_points, format='png')
            chart_buffer_points.seek(0)
            chart_base64_points = base64.b64encode(chart_buffer_points.read()).decode()

            # Clear the current figure
            plt.clf()

            # Create the Assists per Season chart
            plt.figure(figsize=(10, 6))
            plt.bar(seasons, assists, color='orange')
            plt.title(f"Assists per Season for {player_name}")
            plt.xlabel("Season")
            plt.ylabel("Assists")
            plt.xticks(rotation=45, fontsize=10)

            # Save the Assists chart to a BytesIO buffer and encode it as a base64 image
            chart_buffer_assists = BytesIO()
            plt.savefig(chart_buffer_assists, format='png')
            chart_buffer_assists.seek(0)
            chart_base64_assists = base64.b64encode(chart_buffer_assists.read()).decode()

            # Clear the current figure
            plt.clf()

            # Create the Blocks per Season chart
            plt.figure(figsize=(10, 6))
            plt.bar(seasons, blocks, color='green')
            plt.title(f"Blocks per Season for {player_name}")
            plt.xlabel("Season")
            plt.ylabel("Blocks")
            plt.xticks(rotation=45, fontsize=10)

            # Save the Blocks chart to a BytesIO buffer and encode it as a base64 image
            chart_buffer_blocks = BytesIO()
            plt.savefig(chart_buffer_blocks, format='png')
            chart_buffer_blocks.seek(0)
            chart_base64_blocks = base64.b64encode(chart_buffer_blocks.read()).decode()

            # Clear the current figure
            plt.clf()

            # Create the Rebounds per Season chart
            plt.figure(figsize=(10, 6))
            plt.bar(seasons, rebounds, color='red')
            plt.title(f"Rebounds per Season for {player_name}")
            plt.xlabel("Season")
            plt.ylabel("Rebounds")
            plt.xticks(rotation=45, fontsize=10)

            # Save the Rebounds chart to a BytesIO buffer and encode it as a base64 image
            chart_buffer_rebounds = BytesIO()
            plt.savefig(chart_buffer_rebounds, format='png')
            chart_buffer_rebounds.seek(0)
            chart_base64_rebounds = base64.b64encode(chart_buffer_rebounds.read()).decode()

            # Clear the current figure
            plt.clf()

            # Create the Steals per Season chart
            plt.figure(figsize=(10, 6))
            plt.bar(seasons, steals, color='purple')
            plt.title(f"Steals per Season for {player_name}")
            plt.xlabel("Season")
            plt.ylabel("Steals")
            plt.xticks(rotation=45, fontsize=10)

            # Save the Steals chart to a BytesIO buffer and encode it as a base64 image
            chart_buffer_steals = BytesIO()
            plt.savefig(chart_buffer_steals, format='png')
            chart_buffer_steals.seek(0)
            chart_base64_steals = base64.b64encode(chart_buffer_steals.read()).decode()

            # Clear the current figure
            plt.clf()

            # Create the Turnovers per Season chart
            plt.figure(figsize=(10, 6))
            plt.bar(seasons, turnovers, color='gold')
            plt.title(f"Turnovers per Season for {player_name}")
            plt.xlabel("Season")
            plt.ylabel("Turnovers")
            plt.xticks(rotation=45, fontsize=10)

            # Save the Turnovers chart to a BytesIO buffer and encode it as a base64 image
            chart_buffer_turnovers = BytesIO()
            plt.savefig(chart_buffer_turnovers, format='png')
            chart_buffer_turnovers.seek(0)
            chart_base64_turnovers = base64.b64encode(chart_buffer_turnovers.read()).decode()

            # Clear the current figure
            plt.clf()

        plt.figure(figsize=(10, 6))

        plt.bar(seasons, points_FT, label='FT', color='blue')
        plt.bar(seasons, points_2P * 2, label='2P', bottom=points_FT, color='green')
        plt.bar(seasons, points_3P * 3, label='3P', bottom=points_FT + points_2P * 2, color='red')

        plt.title(f"Shots Composition for {player_name}")
        plt.xlabel("Season")
        plt.ylabel("Points")
        plt.xticks(rotation=45, fontsize=10)
        plt.legend()

        # Save the Stacked Bar Chart to a BytesIO buffer and encode it as a base64 image
        chart_buffer_stacked = BytesIO()
        plt.savefig(chart_buffer_stacked, format='png')
        chart_buffer_stacked.seek(0)
        chart_base64_stacked = base64.b64encode(chart_buffer_stacked.read()).decode()

        # Clear the current figure
        plt.clf()
    return render_template("trial.html", player_name=player_name, player_url=image_url, data_1=player_data_1, data_2=player_data_2, data_3=player_data_3, data_4=player_data_4, data_5=player_data_5, chart_base64_points=chart_base64_points, chart_base64_assists=chart_base64_assists, chart_base64_blocks=chart_base64_blocks, chart_base64_rebounds=chart_base64_rebounds, chart_base64_steals=chart_base64_steals, chart_base64_turnovers=chart_base64_turnovers, chart_base64_stacked=chart_base64_stacked, player_profile=player_profile)

if __name__ == "__main__":
    app.run(debug=True)
