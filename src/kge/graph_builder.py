import json
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD

def build_graph(json_file):
    g = Graph()
    # Définition d'un namespace personnalisé pour le projet
    EX = Namespace("http://example.org/videogame/")
    g.bind("ex", EX)

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        # On crée un identifiant unique pour le jeu (en remplaçant les espaces)
        game_id = item['clean_title'].replace(" ", "_").replace(":", "")
        game_uri = URIRef(EX[game_id])

        # Ajout des triplets
        g.add((game_uri, RDF.type, EX.VideoGame))
        g.add((game_uri, EX.hasTitle, Literal(item['clean_title'], datatype=XSD.string)))
        
        if item['detected_platform']:
            platform_uri = URIRef(EX[item['detected_platform'].replace(" ", "_")])
            g.add((game_uri, EX.isPlayedOn, platform_uri))
            g.add((platform_uri, RDF.type, EX.Platform))

    # Sauvegarde au format Turtle
    g.serialize(destination='data/graph.ttl', format='turtle')
    print("Graphe sauvegardé dans data/graph.ttl")

if __name__ == "__main__":
    build_graph('data/processed_games.json')