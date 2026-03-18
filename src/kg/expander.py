import os
from rdflib import Graph

def expand_kb():
    # On récupère le dossier racine du projet (deux niveaux au-dessus de ce script)
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    g = Graph()
    
    # Chemins complets vers tes fichiers
    files_to_load = [
        os.path.join(root_dir, "data", "graph.ttl"),
        os.path.join(root_dir, "ontology.ttl"),
        os.path.join(root_dir, "data", "alignment.ttl")
    ]
    
    for f in files_to_load:
        if os.path.exists(f):
            print(f"Chargement de : {f}")
            g.parse(f, format="turtle")
        else:
            print(f"Erreur : Fichier introuvable -> {f}")

    # Sauvegarde finale
    output_path = os.path.join(root_dir, "data", "expanded.nt")
    g.serialize(destination=output_path, format='nt')
    print(f"\nKB Expansée générée ({len(g)} triplets) dans : {output_path}")

if __name__ == "__main__":
    expand_kb()