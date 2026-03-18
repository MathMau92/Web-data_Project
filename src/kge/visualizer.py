import rdflib
import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(file_path):
    g = rdflib.Graph()
    g.parse(file_path, format="turtle")

    G = nx.DiGraph()

    # On récupère TOUS les triplets pour être sûr de ne rien rater
    for s, p, o in g:
        # On nettoie les noms pour l'affichage (on prend ce qui est après le dernier / ou #)
        s_label = str(s).split('/')[-1].split('#')[-1]
        o_label = str(o).split('/')[-1].split('#')[-1]
        p_label = str(p).split('/')[-1].split('#')[-1]

        # On évite d'afficher le type RDF pour ne pas surcharger (Optionnel)
        if p_label not in ["type", "name"]: 
            G.add_edge(s_label, o_label, label=p_label)

    if len(G.nodes()) == 0:
        print("Attention : Le graphe NetworkX est vide. Vérifie ton fichier .ttl !")
        return

    plt.figure(figsize=(15, 10))
    # Utilisation de shell_layout ou spring_layout pour mieux voir
    pos = nx.spring_layout(G, k=0.8, iterations=50)
    
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="lightgreen", alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.4, edge_color="gray", arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

    plt.title("Réseau des Jeux et Plateformes")
    plt.axis('off')
    
    output_image = "data/graph_viz.png"
    plt.savefig(output_image, bbox_inches='tight')
    print(f"Visualisation réussie ! Image sauvegardée dans {output_image}")
    plt.show()

if __name__ == "__main__":
    visualize_graph("data/graph.ttl")