import logging, argparse
from datetime import datetime
import os, re, requests
from bs4 import BeautifulSoup
import pytz
import sys
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

def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
    }

    response = requests.get(url, headers=headers).content
    soup = BeautifulSoup(response, "html.parser")
    return soup

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


def update_curr_stats(team_name: str, action: str):
    year = 2024

    resp1 = supabase.table("teams").select("transfm_stats_url").eq("team_name", team_name).execute()
    stats_url = resp1.data[0]["transfm_stats_url"]

    resp2 = supabase.table("teams").select("team_id").eq("team_name", team_name).execute()
    team_id = resp2.data[0]["team_id"]

    while year == 2024:
        try:
            soup = get_soup(stats_url)
            trs = get_page_trs(soup)

            for i in trs:
                # all the tds with data
                tds = i.find_all('td')

                squad_num = i.find('td').text

                # check if there is a number
                match = re.search(r'\d', squad_num)
                if not match:
                    continue

                # player name
                name = tds[1].find('span').text
                if name == "":
                    name2 = tds[1].find_all('img')
                    name = name2[-1]['alt']

                resp3 = supabase.table("players").select("player_id").eq("player_name", name).execute()

                if resp3.data and len(resp3.data) > 0:  # check if the response data is not empty
                    player_id = resp3.data[0]["player_id"]
                else:
                    continue

                # minutes
                min = tds[-1].text
                minutes = convert_to_minutes(min)

                # subbed off
                sub_off = tds[-3].text
                match = re.search(r'\d', sub_off)
                if not match:
                    sub_off = 0

                # subbed on
                sub_on = tds[-4].text
                match = re.search(r'\d', sub_on)
                if not match:
                    sub_on = 0

                # red
                red = tds[-5].text
                match = re.search(r'\d', red)
                if not match:
                    red = 0

                # yellows2
                yellows2 = tds[-6].text
                match = re.search(r'\d', yellows2)
                if not match:
                    yellows2 = 0

                # yellows
                yellows = tds[-7].text
                match = re.search(r'\d', yellows)
                if not match:
                    yellows = 0

                # assists
                assists = tds[-8].text
                match = re.search(r'\d', assists)
                if not match:
                    assists = 0

                # goals
                goals = tds[-9].text
                match = re.search(r'\d', goals)
                if not match:
                    goals = 0

                # gp
                gp = tds[-10].text
                match = re.search(r'\d', gp)
                if not match:
                    gp = 0

                # season
                s1 = abs(year) % 100
                s2 = s1 + 1
                season = f"{s1}/{s2}"

                now = datetime.now().isoformat()

                data = {
                    "player_id": player_id,
                    "season": season,
                    "league_id": 9999,
                    "team_id": team_id,
                    "goals": int(goals),
                    "assists": int(assists),
                    "ga": int(goals) + int(assists),
                    "gp": int(gp),
                    "minutes": float(minutes),
                    "yellows": int(yellows),
                    "yellows2": int(yellows2),
                    "reds": int(red),
                    "season_year": year,
                    "squad_number": int(squad_num),
                    "subbed_on": int(sub_on),
                    "subbed_off": int(sub_off),
                    "last_updated": now,
                }

                if action == "insert":
                    try:
                        resp = supabase.table("player_stats").insert(data).execute()
                    except Exception as e:
                        logger.error(f'Error inserting data: {e}')
                elif action == "update":
                    try:
                        resp = supabase.table("player_stats").upsert(data).execute()
                    except Exception as e:
                        logger.error(f'Error updating data: {e}')

        except Exception as e:
            logger.error(f'Error processing year {year}: {e}')

        year = year - 1

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
