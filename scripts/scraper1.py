import logging, argparse
from datetime import datetime
import os, re, requests, sys
from bs4 import BeautifulSoup
import pytz
from dotenv import load_dotenv
import traceback
import json
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

logging.basicConfig(level=logging.INFO, filename="logs/py_log.log", filemode="a", format="%(levelname)s %(asctime)s %(message)s")

logger = logging.getLogger(__name__)

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project root to sys.path
sys.path.append(project_root)

from scripts.functions.common import get_soup, update_curr_stats  

def get_page_trs(soup):
    trs_odd = soup.find_all('tr', class_="odd")
    trs_even = soup.find_all('tr', class_="even")
    return trs_odd + trs_even

def convert_to_minutes(time_string):
    """
    Converts a time string in the
    Args:
        time_string (str): The time string to convert.

    Returns:
        float: The time in minutes, or None if the input is invalid.
    """
    try:
        if "'" in time_string:
            minutes = time_string.replace("'", "")
            minutes2 = float(minutes.replace(".", ""))
            return minutes2
        elif time_string == "-":
            return 0
        else:
            return None  # Invalid format
    except ValueError:
        return None  # Invalid number format



def scrape(team):
    try:
        logger.info(f"Scraping {team}", extra={"team": team})
        response = update_curr_stats(team, "update")
        logger.info(f"Run success {team}")
    except Exception as e:
        logger.error(f"Failed: {team}", exc_info=True)
        raise

def main():
    x = 5
    y = 6
    print(y+x*2)

if __name__ == "__main__":
    main()
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
