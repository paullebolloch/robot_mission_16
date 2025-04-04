# 🤖 Robot Mission 16 – Agent-Based Simulation in a Hostile Environment

Ce projet simule une mission de robots dans un environnement radioactif, chargés de collecter, transformer et transporter des déchets vers une zone sécurisée. Il repose sur une approche **multi-agents (ABM)** utilisant la librairie **Mesa** et la visualisation **Solara**.

---

## 📁 Structure du projet

### `model.py`
Définit le modèle principal `MyModel`, l'environnement (`MultiGrid`), les agents (robots et objets), et leurs placements dans les différentes zones (z1, z2, z3). Contiendra la méthode `do()` qui exécute les actions des agents et renvoie leurs perceptions.

### `agents.py`
Contient les classes d’agents **mobiles** (robots). Chaque robot implémentera à terme une boucle :
- `percepts` → perception de l’environnement,
- `deliberate` → décision de l’action à entreprendre,
- `do` → exécution de l’action.

*Actuellement : un agent simple avec déplacement aléatoire (`MyAgent`).*

### `objects.py`
Regroupe les **agents inanimés** :
- `RadioactivityAgent` : cellule fixe avec zone (`z1`, `z2`, `z3`) et niveau de radioactivité aléatoire.
- `WasteDisposalZone` : cellule noire où les déchets sont déposés (radioactivité = -1).
- `Waste` : objets à collecter, de différentes couleurs (green, yellow, red).

### `server.py`
Interface visuelle basée sur `Solara`. Décrit comment afficher chaque type d’agent et lance l’interface interactive via `SolaraViz`.

### `run.py`
Fichier de lancement prévu pour exécuter la simulation en ligne de commande ou en batch (actuellement vide).

---

## 🚧 Objectifs pédagogiques

Ce projet s’inscrit dans un enseignement sur les systèmes multi-agents et modélise une mission inspirée de cas réels.

### Étapes du développement :
1. ✅ **Implémentation de l’environnement et des objets**
2. 🟡 **Ajout des comportements des robots (perception, délibération, action)**
3. ⏳ **Collaboration et communication entre agents**
4. ⏳ **Gestion des incertitudes**

---

## ▶️ Lancer l'interface

```bash
solara run server.py
