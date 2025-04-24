import logging, argparse, pytz, json, traceback
from datetime import datetime
import os, re, requests, sys, random
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from termcolor import colored, cprint
# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the project root to sys.path
sys.path.append(project_root)
from scripts.utils.supabase_cli import supabase
from scripts.functions.update_tables import update_team_transfm_info

def scrape(team_id):
    try:
        update_team_transfm_info(team_id)
    except Exception as e:
        print(e)
        print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('league_id', type=int, help='The league ID to process')
    #parser.add_argument('season', type=int, help='Year of the ranking')
    args = parser.parse_args()

    #print(f"Processing league ID: {args.league_id}")
    # REPLACE LEAGUE ID
    # 2 = GB1
    #player_id = 36633
    response = supabase.table("teams").select("transfm_id").eq("league_id", args.league_id).execute()
    #logger.info(f'Scraping League {args.league_id} Teams Info')
    cprint(f"Scraping League {args.league_id}")
    #scrape(args.league_id)
    
    for i in response.data:
        id = i["transfm_id"]
        scrape(id)
        print(f'Team {id} done')





