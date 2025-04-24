import re, requests, sys, json, random, os, re, logging, argparse
from termcolor import colored, cprint
from pprint import pprint
# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the project root to sys.path
sys.path.append(project_root)
from scripts.utils.supabase_cli import RAPID_API_KEY
from scripts.utils.supabase_cli import supabase

GLOBAL_YEAR = 2024

logging.basicConfig(level=logging.INFO, filename="logs/py_log.log", filemode="a", format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

headers = {
	    "x-rapidapi-key": RAPID_API_KEY,
	    "x-rapidapi-host": "transfermarkt-db.p.rapidapi.com"
}

def get_player_info(player_id: int):
    url = "https://transfermarkt-db.p.rapidapi.com/v1/players/info"
    querystring = {"player_id": player_id,"locale":"US"}
    response = requests.get(url, headers=headers, params=querystring)
    
    data = response.json()
    club_name = data["data"]["details"]["club"]["fullName"]
    short_club_name = data["data"]["details"]["club"]["name"]

    name = data["data"]["details"]["player"]["name"]

    if club_name != "Retired":
        dom_league = data["data"]["details"]["club"]["mainCompetition"]["name"]
        short_dom_league = data["data"]["details"]["club"]["mainCompetition"]["shortName"]
        #cprint(dom_league, "cyan")
    else:
        dom_league = None
        short_dom_league = None
    #json_res = json.dumps(name, indent=4)
    #cprint(name, "cyan")
    #data_object = json.loads(response)

    #name = data[0]
    #cprint(data[0], "light_magenta")
    return name, club_name, short_club_name, dom_league, short_dom_league 

def get_league_rankings(comp_id: str, year: int, id: int):
    url = "https://transfermarkt-db.p.rapidapi.com/v1/competitions/standings"
    querystring = {"competition_id": comp_id,"locale":"US","standing_type":"general","season_id":year}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    league_name = data["data"]["share"]["title"]
    suffix_to_remove = " - Table"
    if league_name.endswith(suffix_to_remove):
        league_name = league_name[:-len(suffix_to_remove)]
    
    table = data["data"]["table"]
    #t2 = data["data"]["details"]["club"]["name"]

    for i in table:
        club = i["clubName"]
        club_id = i["id"]
        logo_url = i["clubImage"].replace("medium", "big")
        rank = i["rank"]
        points = i["points"]
        matches = i["matches"]
        wins = i["wins"]
        losses = i["losses"]
        draws = i["draw"]

        goals = i["goals"]
        goalsConceded = i["goalsConceded"]
        goalDifference = i["goalDifference"]
        info = i["markDescription"]

        cprint(f"{rank}. {club} | GF {goals} GA {goalsConceded}", "light_green")
        cprint(f"{points} | W{wins} D{draws} L{losses} ", "cyan")
        #cprint(f"gf {goals}", "light_red")
        
        # GET the team ID from DB with Team names
        
        
        resp1 = supabase.table("teams").select("team_id").eq("team_name", club).execute()
        if resp1.data:
            team_id = resp1.data[0]['team_id']
            cprint(f"TeamID {team_id} found!", "yellow")
        else:
            
            cprint(f"Club {club} needs to be inserted", "red")
            #cprint(resp1, "red")
            team_id = random.randint(10000,99999)
            data_object = {
                    "team_name": club,
                    "transfm_id": club_id,
                    "logo_url": logo_url,
                    "team_id": team_id,
                    "league_id": id
            }
            resp1 = supabase.table("teams").insert(data_object).execute()
            cprint(resp1, "light_magenta")
            print(f"NEW Team {club}")
            print("\n")
            logger.info(f"NEW TEAM INSERTED: {club}")
            logger.info(resp1)
            #sys.exit(1)

        data_object = {
            "team_id": team_id,
            "comp_id": id,
            "season_year": year,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "points": points,
            "gd": goalDifference,
            "gp": matches,
            "goals_f": goals,
            "goals_a": goalsConceded,
            "info": info,
            "rank": rank,
            "rank_id": random.randint(10000,99999)
        }
        
        try:
            resp = supabase.table("league_ranks").insert(data_object).execute()
            if resp.data:
            #cprint(f"Error inserting {club}", "red")
                cprint(resp, "light_magenta")
                logger.info(f'INSERT ATTEMPT: {club}')
                logger.info(resp)
        except Exception as e:
            cprint(f"Error inserting {club}", "light_red")
            logger.error(f"Error insert attempt {club}")
            logger.error(e)
            print(e)


            cprint("Update_instead", "blue")
            del data_object["rank_id"]
            #cprint(data_object, "blue")

            if year == GLOBAL_YEAR:
                try:
                    resp = supabase.table("league_ranks").upsert(data_object).execute()
                    if resp.data:
                        #cprint(f"Error inserting {club}", "red")
                        cprint(resp, "light_magenta")
                        logger.info(f'UPDATE ATTEMPT: {club}')
                        logger.info(resp)
                except Exception as e:
                    cprint(f"Error UPDATING {club}", "light_red")
                    logger.error(f"Error UPDATING attempt {club}")
                    logger.error(e)
                    print(e)


        
        
    #t3 = data["data"]["details"]["player"]["name"]
    cprint(league_name, "cyan")
    #cprint(table, "light_green")

max = 1995
def get_team_info(id: int):
    url = "https://transfermarkt-db.p.rapidapi.com/v1/clubs/profile"

    querystring = {"locale":"US","club_id": id} 

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    name = data["data"]["mainFacts"]["fullName"]
    transfm_id = data["data"]["mainFacts"]["id"]
    transfm_bio_url = data["data"]["share"]["url"]
    city = data["data"]["mainFacts"]["city"]
    stadium = data["data"]["stadium"]["name"]
    trophies = data["data"]["successes"]
    #name = data["data"]["mainFacts"]["fullName"]

    cprint(name, "green")
    #cprint(f'{city} - {stadium}', "green")
    #cprint(len(trophies), "blue")
    
    for i in range(len(trophies)-1, -1, -1): 
        comp = trophies[i]["additionalData"]["competitionId"]

        resp = supabase.table("leagues").select("league_id").eq("transfm_name", comp).execute()
        if resp.data:
            x=1
            cprint(comp, "blue")
        else:
            del trophies[i]
            #continue

    response = supabase.table("teams").select("team_id").eq("transfm_id", transfm_id).execute()
    team_id = response.data[0]['team_id']
        
    data_object = {
            "team_id": team_id,
            "transfm_id": transfm_id,
            "transfm_bio_url": transfm_bio_url,
            "city": city,
            "stadium": stadium,
            "trophies": trophies,
    }
    
    return data_object


