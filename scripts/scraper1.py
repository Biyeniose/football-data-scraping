import logging, argparse
from datetime import datetime
import os, re, requests, sys
from bs4 import BeautifulSoup
import pytz
from dotenv import load_dotenv
import traceback
import json

logging.basicConfig(level=logging.INFO, filename="logs/py_log.log", filemode="a", format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the project root to sys.path
sys.path.append(project_root)
from scripts.utils.supabase_cli import supabase
from scripts.functions.common import get_soup  
from scripts.functions.update_curr_season import update_curr_stats

def scrape(team):
    try:
        logger.info(f"Scraping {team}", extra={"team": team})
        response = update_curr_stats(team, "update")
        logger.info(f"Run success {team}")
    except Exception as e:
        logger.error(f"Failed: {team}", exc_info=True)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('league_id', type=int, help='The league ID to process')
    args = parser.parse_args()

    print(f"Processing league ID: {args.league_id}")
    # REPLACE LEAGUE ID
    epl_teams = supabase.table("teams").select("team_name").eq("league_id", args.league_id).execute()

    for i in epl_teams.data:
        team_name = i["team_name"]
        scrape(team_name)
        print(f'Team {i} done')
