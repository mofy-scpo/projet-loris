# Observatoire des Établissements Scolaires Fermés

Tableau de bord cartographique et statistique des établissements scolaires fermés en France, à partir de la base publique de la DEPP (Ministère de l'Éducation nationale).

**🔗 Site en ligne :** https://MarcOFlaherty.github.io/projet-loris/

## Fonctionnalités

- **Carte interactive** de la France (régions / départements) avec dégradé de densité des fermetures.
- **KPI** : total des établissements fermés, maternelles & élémentaires, collèges & lycées.
- **Graphiques** : évolution des fermetures par année, principaux types fermés, structure par degré.
- **Annuaire** filtrable et paginé (recherche par nom, commune, UAI ; filtres par année et par type).
- **Filtrage géographique** : un clic sur une région ou un département recentre la carte et filtre l'ensemble du tableau de bord.

## Source des données

Données publiques du jeu de données `fr-en-etablissements-fermes`, interrogées en direct via l'API Opendatasoft de l'Éducation nationale :

```
https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-etablissements-fermes/records
```

Portail : https://data.education.gouv.fr/explore/dataset/fr-en-etablissements-fermes/

## Architecture

Site 100 % statique, sans backend. Les statistiques et l'annuaire sont récupérés côté client depuis l'API DEPP.

| Fichier | Rôle |
|---------|------|
| `index.html` | Structure du tableau de bord |
| `index.css` | Styles (thème sombre) |
| `app.js` | Logique : appels API, KPI, graphiques (Chart.js), tableau, filtres |
| `map.html` | Carte Folium pré-générée (intégrée en iframe) |
| `build_map.py` | Script de génération de la carte |

## Régénérer la carte

La carte `map.html` est un artefact généré. Pour la reconstruire (agrégats par région/département) :

```bash
pip install -r requirements.txt
python build_map.py
```

Le script télécharge les GeoJSON des régions et départements, récupère les agrégats depuis l'API DEPP, puis écrit `map.html`.

## Déploiement

Le site est publié automatiquement via **GitHub Pages** (branche `main`, racine du dépôt). Tout `push` sur `main` met le site à jour.

## 🚀 Pistes d'Évolution & Défis (Roadmap pour Loris)

Pour transformer ce tableau de bord en un observatoire d'impact national multi-sources, voici les prochains défis d'implémentation proposés :

### 🟢 Défi 1 : Intégrer les Ouvertures et calculer le "Solde Net"
* **Objectif** : Ne pas afficher uniquement les fermetures, mais mesurer le renouvellement scolaire.
* **Méthode** : 
  - Croiser le jeu de données des fermetures avec celui des écoles actives : `fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre` (qui contient la `date_ouverture` des écoles encore ouvertes).
  - Fusionner les deux sources pour obtenir le nombre total d'ouvertures par an et calculer le solde net : $\text{Solde Net} = \text{Ouvertures} - \text{Fermetures}$.
  - Ajouter un graphique comparatif Vert (Ouvertures) / Rouge (Fermetures) dans le dashboard.
* *Un script de démonstration fonctionnel en Python a été déposé dans [test_solde_net.py](test_solde_net.py) pour servir de modèle et valider l'API.*

### 🔵 Défi 2 : Corrélation Démographique (INSEE)
* **Objectif** : Déterminer scientifiquement si les fermetures d'écoles sont directement corrélées à la baisse locale de la population.
* **Méthode** :
  - Récupérer les données historiques des populations communales de l'INSEE (particulièrement la tranche d'âge **0-14 ans**).
  - Calculer le taux de variation démographique sur les 5 à 10 ans précédant la fermeture d'une école.
  - Afficher un graphique de corrélation (nuage de points) et ajouter la courbe de population historique sur la vue détaillée d'une commune.

### 🟡 Défi 3 : Modèle Prédictif (Machine Learning)
* **Objectif** : Créer un outil prédictif capable d'estimer la probabilité de fermeture d'une école encore ouverte à horizon 3-5 ans.
* **Méthode** : 
  - Entraîner un modèle de classification (ex: Random Forest, XGBoost) avec comme caractéristiques (*features*) : la tendance démographique locale (0-14 ans), les effectifs scolaires (IPS), la distance géographique à l'école active la plus proche, et la santé budgétaire de la commune (dette, dotations de l'État).
  - Exporter le modèle pour l'intégrer au dashboard sous forme de simulateur interactif pour les communes.

### 🟤 Défi 4 : Autres Croisements Open Data
* **Finances Locales** : Relier les fermetures avec le niveau d'endettement ou la Dotation Globale de Fonctionnement (DGF) des communes (données DGCL sur data.gouv.fr).
* **Désertification** : Croiser avec la Base Permanente des Équipements (BPE) de l'INSEE pour voir si la fermeture de l'école accélère la disparition des commerces de proximité et des médecins.
* **Bilan Carbone** : Estimer la distance supplémentaire parcourue par les élèves après la fermeture de leur école de proximité pour en déduire l'impact CO2 induit par le transport scolaire.

