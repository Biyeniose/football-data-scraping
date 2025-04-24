import logging, argparse
from datetime import datetime   
import os, re, requests, sys
from bs4 import BeautifulSoup
import pytz
from dotenv import load_dotenv
import traceback
import json
from termcolor import colored, cprint

logging.basicConfig(level=logging.INFO, filename="logs/py_log.log", filemode="a", format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the project root to sys.path
sys.path.append(project_root)
from scripts.utils.supabase_cli import supabase
from scripts.functions.transfm_api import get_league_rankings

def scrape(id, season):

    resp = supabase.table("leagues").select("transfm_name").eq("league_id", id).execute()
    if resp.data:
        print(f"League ID found {id}")
    else:
        sys.exit(1)
    try:
        cprint(f"Scraping {id}", "yellow")
        #response = get_player_info(126414)
        get_league_rankings(resp.data[0]["transfm_name"], season, id)
        #cprint(name, "light_green")
        #cprint(curr_team, "light_green")
        #cprint(league, "light_green")

    except Exception as e:
        #logger.error(f"Failed: {team}", exc_info=True)
        cprint(f"Failed: {id}", "red")
        print(e)
        print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('league_id', type=int, help='The league ID to process')
    parser.add_argument('season', type=int, help='Year of the ranking')
    args = parser.parse_args()

    #print(f"Processing league ID: {args.league_id}")
    # REPLACE LEAGUE ID
    # 2 = GB1
    #player_id = 36633
    #response = supabase.table("players").select("transfm_id").eq("player_id", player_id).execute()
    logger.info(f'Scraping League Rankings: ID {args.league_id} Year {args.season}')
    scrape(args.league_id,args.season)
    logger.info(f'RUN FINISHED ID {args.league_id} Year {args.season}')
    #for i in response.data:
        #id = i["transfm_id"]
        #scrape(id)
        #print(f'Player {id} done')



