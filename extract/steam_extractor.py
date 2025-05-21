import requests
import json
import sys
import os
from time import sleep
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger


log = setup_logger(__name__)

def get_game_data(appid):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()

        return data
    
    except requests.exceptions.RequestException as e:
        log.info(f"Error on request: {e}")
        raise


def get_top_played_games(limit: int | None = None) -> list:
    url = "https://steamspy.com/api.php?request=top100in2weeks"
    
    try:
        sleep(1)
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        top_games = []
        for appid, game_data in data.items():
            if len(top_games) >= limit:
                break
                
            top_games.append({
                "appid": appid
            })
        
        return top_games
    
    except requests.exceptions.RequestException as e:
        log.info(f"Error on request: {e}")
        raise


def main():
    log.info("Getting the most played games in the last 2 weeks...")
    top_games = get_top_played_games(limit=20)

    dataset_steam = []

    for game in top_games:
        appid = game["appid"]
        log.info(f"Processing appid: {appid}")
        game_data = get_game_data(appid)

        filtered_data = {
            "appid": int(game_data["appid"]),
            "game_name": game_data.get("name"),
            "price": float(game_data.get("price", "0")) / 100,
            "free": game_data.get("price", "0") == "0"
        }

        dataset_steam.append(filtered_data)

    with open("dataset_steam.json", "w", encoding="utf-8") as f:
        json.dump(dataset_steam, f, ensure_ascii=False, indent=4)

    log.info("File 'dataset_steam.json' saved successfully.")


if __name__ == "__main__":
    main()
