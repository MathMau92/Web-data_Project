import json
import requests
import time
from rdflib import Graph, URIRef, Namespace, OWL

def get_dbpedia_uri(game_title):
    """Cherche l'URI DBpedia via l'API de recherche."""
    url = "https://lookup.dbpedia.org/api/search"
    params = {'query': game_title, 'format': 'json', 'limit': 1}
    try:
        res = requests.get(url, params=params)
        data = res.json()
        if data['docs']:
            return data['docs'][0]['resource'][0] # Retourne l'URL de la ressource
    except:
        return None
    return None

def generate_alignment():
    EX = Namespace("http://example.org/vg/")
    g = Graph()
    g.bind("ex", EX)
    g.bind("owl", OWL)

    with open('data/processed_games.json', 'r', encoding='utf-8') as f:
        games = json.load(f)

    print("Début de l'alignement avec DBpedia...")
    for game in games[:20]: # On teste sur les 20 premiers pour ne pas être banni par l'API
        title = game['clean_title']
        dbpedia_uri = get_dbpedia_uri(title)
        
        if dbpedia_uri:
            local_uri = EX[title.replace(" ", "_").replace(":", "")]
            g.add((local_uri, OWL.sameAs, URIRef(dbpedia_uri)))
            print(f"Aligné : {title} -> {dbpedia_uri}")
        
        time.sleep(0.5) # Eviter de DDOS

    g.serialize(destination='data/alignment.ttl', format='turtle')
    print("\nFichier alignment.ttl généré dans /data !")

if __name__ == "__main__":
    generate_alignment()