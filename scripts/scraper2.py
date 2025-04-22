import logging, argparse
from datetime import datetime
import os, re, requests, sys
from bs4 import BeautifulSoup
import pytz
from dotenv import load_dotenv
import traceback
import json
from termcolor import colored, cprint
# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the project root to sys.path
sys.path.append(project_root)
from scripts.utils.supabase_cli import supabase
from scripts.functions.transfm_api import get_player_info

def scrape(id):
    try:
        cprint(f"Scraping {id}", "yellow")
        #response = get_player_info(126414)
        name, curr_team, short_team, league, short_league = get_player_info(id)
        cprint(name, "light_green")
        cprint(curr_team, "light_green")
        cprint(league, "light_green")

    except Exception as e:
        #logger.error(f"Failed: {team}", exc_info=True)
        cprint(f"Failed: {id}", "red")
        print(e)
        print("\n")


if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument('league_id', type=int, help='The league ID to process')
    #args = parser.parse_args()

    #print(f"Processing league ID: {args.league_id}")
    # REPLACE LEAGUE ID
    # 2 = GB1
    player_id = 36633
    response = supabase.table("players").select("transfm_id").eq("player_id", player_id).execute()

    for i in response.data:
        id = i["transfm_id"]
        scrape(id)
        print(f'Player {id} done')





