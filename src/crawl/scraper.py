import cloudscraper
from bs4 import BeautifulSoup
import time

def get_games_list(url):
    # Création du scraper pour passer les protections
    scraper = cloudscraper.create_scraper()
    
    try:
        print(f"Tentative de crawl sur : {url}")
        response = scraper.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # On cible les liens qui contiennent les titres des tests
            # La classe 'layout-content' contient souvent le corps de la page
            content_area = soup.find('main') # On se limite au contenu principal
            
            game_titles = []
            if content_area:
                # On cherche les titres de jeux (souvent dans des balises <a> avec une classe spécifique)
                # Teste cette classe qui est courante chez eux :
                links = content_area.find_all('a', class_='link-stretching')
                
                for link in links:
                    title = link.get_text().strip()
                    if title and len(title) > 2:
                        game_titles.append(title)

            # Si la liste est toujours vide, on essaie une approche plus large
            if not game_titles:
                # Chercher tous les h2 ou h3 qui ne sont pas dans le header/footer
                for h in soup.find_all(['h2', 'h3']):
                    name = h.get_text().strip()
                    if name: game_titles.append(name)
            
            return list(set(game_titles)) # Utilise set() pour éviter les doublons
        else:
            print(f"Erreur {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Erreur : {e}")
        return []

if __name__ == "__main__":
    url = "https://www.jeuxvideo.com/tests/"
    games = get_games_list(url)
    
    if games:
        print(f"\nSuccès ! On a trouvé {len(games)} éléments :")
        for g in games[:10]: # On affiche les 10 premiers
            print(f"- {g}")
    else:
        print("Aucune donnée trouvée.")