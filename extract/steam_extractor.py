import requests
import json
import sys
import os
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger

log = setup_logger(__name__)

def get_top_played_games(limit=None):
    url = "https://steamcharts.com/top"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    gamelist = []
    rows = soup.select('table tr')[1:limit+1] if limit else soup.select('table tr')[1:]
    
    for row in rows:
        cols = row.find_all('td')
        appid = cols[1].find('a')['href'].split('/')[2]
        gamelist.append(appid)
    
    return gamelist


def get_data_appdetails(appid):
    try:
        sleep(1)
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        log.error(f"Error fetching data for appid {appid}: {e}")
        raise


def get_data_current_players(appid):
    try:
        sleep(1)
        url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        player_cnt = data.get('response').get('player_count')
        return player_cnt
    except requests.exceptions.RequestException as e:
        log.error(f"Error fetching data for appid {appid}: {e}")
        raise


def get_data_2weeks_avg_players(appid):
    try:
        url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        avg_players = data.get('average_2weeks')
        return avg_players
    except requests.exceptions.RequestException as e:
        log.error(f"Error fetching data for appid {appid}: {e}")
        raise


def extract_game_data(appid, app_data):
    try:

        game_info = {
            "appid": int(appid),
            "game_name": app_data.get('name', ''),
            "is_free": app_data.get('is_free', False),
            "language": app_data.get('supported_languages', ''),
            "developer": app_data.get('developers', []),
            "publisher": app_data.get('publishers', []),
            "platform": app_data.get('platforms', {}),
            "recommendations": app_data.get('recommendations', {}).get('total', 0)
        }

        
        package_groups = app_data.get('package_groups', [])
        subs_list = []
        
        for group in package_groups:
            subs = group.get('subs', [])
            subs_list.extend(subs)
        
        game_info['price'] = subs_list

        
        game_info['genre'] = [g['description'] for g in app_data.get('genres', [])]
        game_info['category'] = [c['description'] for c in app_data.get('categories', [])]

        return game_info
    except Exception as e:
        log.error(f"Error processing data for appid {appid}: {e}")
        raise


def main():
    dataset_steam = []
    top_played_games = get_top_played_games(10)
    
    for appid in top_played_games:
        log.info(f"Processing appid: {appid}")
        try:
            game_data = get_data_appdetails(appid)
            if not game_data or str(appid) not in game_data or not game_data[str(appid)].get('success', False):
                log.warning(f"Skipping appid {appid} - data not available")
                continue

            app_data = game_data[str(appid)]['data']
            filtered_data = extract_game_data(appid, app_data)
            
            
            if filtered_data:
                try:
                    current_players = get_data_current_players(appid)
                    filtered_data['current_players'] = current_players
                except Exception as e:
                    log.warning(f"Could not fetch current player count for appid {appid}: {e}")
                    filtered_data['current_players'] = None

                try:
                    avg_players = get_data_2weeks_avg_players(appid)
                    filtered_data['avg_players_two_weeks'] = avg_players
                except Exception as e:
                    log.warning(f"Could not fetch average players count for appid {appid}: {e}")
                    filtered_data['avg_players_two_weeks'] = None

                dataset_steam.append(filtered_data)
                log.info(f"Successfully processed: {filtered_data['game_name']}")
            else:
                log.warning(f"Failed to process data for appid {appid}")

        except Exception as e:
            log.error(f"Error processing appid {appid}: {e}")
            continue

    with open('steam_top_games.json', 'w', encoding='utf-8') as f:
        json.dump(dataset_steam, f, ensure_ascii=False, indent=2)
    
    log.info(f"Successfully processed {len(dataset_steam)} games")
    return dataset_steam


if __name__ == "__main__":
    result = main()
    if isinstance(result, list):
        df = pd.DataFrame(result)
    else:
        df = result
    
    df.to_csv('df.csv', index=False)