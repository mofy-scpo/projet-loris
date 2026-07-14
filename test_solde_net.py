import urllib.request
import json
from collections import defaultdict

def fetch_json(url):
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def main():
    print("=== Preuve de Concept : Calcul du Solde Net d'Écoles ===")
    
    # 1. API Écoles Actives : Nombre d'ouvertures par année de 'date_ouverture'
    url_actives = (
        "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
        "fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/records"
        "?group_by=year(date_ouverture)"
        "&select=year(date_ouverture)%20as%20annee,count(numero_uai)%20as%20total"
        "&order_by=year(date_ouverture)%20asc"
        "&limit=150"
    )
    
    # 2. API Écoles Fermées : Nombre d'ouvertures par année de 'date_ouverture'
    url_fermees_ouvertures = (
        "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
        "fr-en-etablissements-fermes/records"
        "?group_by=year(date_ouverture)"
        "&select=year(date_ouverture)%20as%20annee,count(numero_uai)%20as%20total"
        "&order_by=year(date_ouverture)%20asc"
        "&limit=150"
    )
    
    # 3. API Écoles Fermées : Nombre de fermetures par année de 'date_fermeture'
    url_fermees_fermetures = (
        "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
        "fr-en-etablissements-fermes/records"
        "?group_by=year(date_fermeture)"
        "&select=year(date_fermeture)%20as%20annee,count(numero_uai)%20as%20total"
        "&order_by=year(date_fermeture)%20asc"
        "&limit=150"
    )
    
    openings_per_year = defaultdict(int)
    closures_per_year = defaultdict(int)
    
    print("\n[1/3] Récupération des ouvertures d'écoles actuellement ACTIVES...")
    try:
        res = fetch_json(url_actives)
        for r in res.get('results', []):
            year_val = r.get('year(date_ouverture)')
            if year_val is not None:
                openings_per_year[int(year_val)] += r.get('total', 0)
    except Exception as e:
        print(f"Erreur API Actives: {e}")
        
    print("[2/3] Récupération des ouvertures historiques d'écoles aujourd'hui FERMÉES...")
    try:
        res = fetch_json(url_fermees_ouvertures)
        for r in res.get('results', []):
            year_val = r.get('year(date_ouverture)')
            if year_val is not None:
                openings_per_year[int(year_val)] += r.get('total', 0)
    except Exception as e:
        print(f"Erreur API Fermées (ouvertures): {e}")

    print("[3/3] Récupération des fermetures d'écoles par année de fermeture...")
    try:
        res = fetch_json(url_fermees_fermetures)
        for r in res.get('results', []):
            year_val = r.get('year(date_fermeture)')
            if year_val is not None:
                closures_per_year[int(year_val)] += r.get('total', 0)
    except Exception as e:
        print(f"Erreur API Fermées (fermetures): {e}")

    # Affichage du bilan pour les années récentes (2010 - 2025)
    print("\nBilan annuel (2010 - 2025) :")
    print(f"{'Année':<8} | {'Ouvertures':<10} | {'Fermetures':<10} | {'Solde Net':<10}")
    print("-" * 46)
    
    for year in sorted(range(2010, 2026)):
        openings = openings_per_year[year]
        closures = closures_per_year[year]
        net_balance = openings - closures
        
        # Coloration simple dans la console
        if net_balance > 0:
            status = f"+{net_balance} 🟢"
        elif net_balance < 0:
            status = f"{net_balance} 🔴"
        else:
            status = "0 ⚪"
            
        print(f"{year:<8} | {openings:<10} | {closures:<10} | {status:<10}")

if __name__ == "__main__":
    main()
