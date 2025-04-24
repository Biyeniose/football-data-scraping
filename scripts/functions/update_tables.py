import re, requests, sys, json, random, os, re, logging, argparse
from termcolor import colored, cprint
from pprint import pprint
# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the project root to sys.path
sys.path.append(project_root)
from scripts.utils.supabase_cli import supabase
from scripts.functions.transfm_api import get_team_info

logging.basicConfig(level=logging.INFO, filename="logs/py_log.log", filemode="a", format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

max=1995

# function for using the Transfm API and getting team data
def update_team_transfm_info(team_id: int):
    team_data = get_team_info(team_id)
    
    team_id = team_data["team_id"]
    #cups = team_data['trophies']
    cups = team_data['trophies'] # this is all the finishes

    for i in cups:
        #name = cups[0]['name']
        #name = cups['name']
        #seasons = team_data['trophies']['seasonIds']

        #cprint(team_data, "yellow")
        #cprint(cups, "cyan")
        cprint(i, "red")
        comp_id = i["additionalData"]['competitionId']
        years = i["additionalData"]['seasonIds']

        response = supabase.table("leagues").select("league_id").eq("transfm_name", comp_id).execute()
        league_id = response.data[0]['league_id']

        for j in years:
        # for i in each season insert into league_ranks table
            season_year = int(j)
            data_object = {
                "team_id": team_id,
                "season_year": season_year,
                "comp_id": league_id,
                "rank": 1,
                "round": "Winners",
                "rank_id": random.randint(10000,99999)
            }

            #cprint(data_object, "blue")
            try:
                response = supabase.table("league_ranks").insert(data_object).execute()


                cprint(response, "magenta")
                logger.info(response)
            except Exception as e:
                # You can also specify 0-255 RGB ints via a tuple
                cprint("Error inserting", "light_red")

                logger.error(e)
            














