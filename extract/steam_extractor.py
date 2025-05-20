import requests
import json
import time
from utils.logger import setup_logger

log = setup_logger(__main__)

def fetch_and_save_reviews(appid):
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&day_range=1&language=all"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            reviews_data = response.json()
            output_file = f"reviews_steam_{appid}.json"
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(reviews_data, file, indent=4, ensure_ascii=False)
            log.info(f"Reviews salvas em: {output_file}")
        else:
            log.error(f"Erro no appID {appid}: Status Code {response.status_code}")
    except Exception as e:
        log.error(f"Erro no appID {appid}: {str(e)}")
        raise