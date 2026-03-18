import spacy
from spacy.pipeline import EntityRuler
import re
import json

def os_setup_nlp():
    """Configure spaCy avec des règles spécifiques au Gaming."""
    nlp = spacy.load("fr_core_news_sm")
    
    # On ajoute un 'EntityRuler' pour corriger les erreurs de l'IA de base
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    
    # On définit des patterns prioritaires (Tu pourras en ajouter d'autres)
    patterns = [
        {"label": "GAME", "pattern": [{"LOWER": "elden"}, {"LOWER": "ring"}]},
        {"label": "GAME", "pattern": [{"LOWER": "mario"}, {"LOWER": "tennis"}]},
        {"label": "PLATFORM", "pattern": [{"LOWER": "ps5"}]},
        {"label": "PLATFORM", "pattern": [{"LOWER": "switch"}]},
        {"label": "PLATFORM", "pattern": [{"LOWER": "pc"}]},
        {"label": "PLATFORM", "pattern": [{"LOWER": "xbox"}]}
    ]
    ruler.add_patterns(patterns)
    return nlp

def clean_title(raw_title):
    """Nettoie le titre brut issu du scraping."""
    # Enlever 'Test' ou 'Test ' au début (insensible à la casse)
    text = re.sub(r'^[Tt]est\s*', '', raw_title)
    
    # Séparer le nom du jeu et la plateforme si ' sur ' est présent
    parts = re.split(r'\s+sur\s+', text, flags=re.IGNORECASE)
    
    game_name = parts[0].strip()
    platform_hint = parts[1].strip() if len(parts) > 1 else None
    
    return game_name, platform_hint

def extract_entities(text, nlp):
    """Utilise l'IA pour extraire et classifier les entités."""
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        # Correction manuelle : si l'IA persiste à mettre PER pour un titre de jeu
        label = ent.label_
        if label == "PER" and any(word in ent.text.lower() for word in ["ring", "mario", "zelda", "fantasy"]):
            label = "GAME"
            
        entities.append({
            "text": ent.text,
            "type": label
        })
    return entities

def process_raw_titles(titles_list):
    """Pipeline principale d'extraction."""
    nlp = os_setup_nlp()
    results = []
    
    for raw in titles_list:
        game_name, platform_hint = clean_title(raw)
        entities = extract_entities(game_name, nlp)
        
        results.append({
            "raw": raw,
            "clean_title": game_name,
            "detected_platform": platform_hint,
            "entities": entities
        })
    
    return results

if __name__ == "__main__":
    # Liste de test basée sur tes résultats de crawl
    sample_data = [
        "TestMario Tennis Fever sur Switch 2",
        "TestElden Ring sur PS5",
        "TestResident Evil Requiem",
        "TestYakuza Kiwami 3 & Dark Ties sur PC"
    ]
    
    final_data = process_raw_titles(sample_data)
    print(json.dumps(final_data, indent=4, ensure_ascii=False))