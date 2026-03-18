import json
import os
import time
from crawl.scraper import get_games_list
from ie.extractor import process_raw_titles

def run_project_pipeline(nb_pages=2):
    all_titles = []
    
    print(f"--- Étape 1 : Crawling de {nb_pages} pages ---")
    for i in range(1, nb_pages + 1):
        url = f"https://www.jeuxvideo.com/tests/?p={i}"
        print(f"Page {i}...")
        titles = get_games_list(url)
        all_titles.extend(titles)
        time.sleep(1) # Éthique : on attend un peu entre les pages

    print(f"--- Étape 2 : Extraction (IE) de {len(all_titles)} éléments ---")
    final_data = process_raw_titles(all_titles)

    print(f"--- Étape 3 : Sauvegarde ---")
    os.makedirs('data', exist_ok=True)
    with open('data/processed_games.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)
    
    print("Succès ! Données disponibles dans data/processed_games.json")

if __name__ == "__main__":
    run_project_pipeline()