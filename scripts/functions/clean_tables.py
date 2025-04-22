import re, requests, sys, json, random, os, re, logging, argparse
from termcolor import colored, cprint
from pprint import pprint
# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the project root to sys.path
sys.path.append(project_root)
from scripts.utils.supabase_cli import RAPID_API_KEY
from scripts.utils.supabase_cli import supabase
from scripts.functions.transfm_api import get_team_info

logging.basicConfig(level=logging.INFO, filename="logs/py_log.log", filemode="a", format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

headers = {
	    "x-rapidapi-key": RAPID_API_KEY,
	    "x-rapidapi-host": "transfermarkt-db.p.rapidapi.com"
}


# function for using the Transfm API and getting team data
def update_team_transfm_info(team_id: int):
    get_league_rankings(team_id)











