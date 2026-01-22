# Auto-Clicker

Application d'auto-clicker moderne avec interface graphique, développée en Python.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## Fonctionnalités

### Mode Clic Simple
- Intervalle entre clics configurable (en millisecondes)
- Type de clic : Gauche, Droit ou Molette
- Répétitions : infinies ou nombre limité
- Position : suivre le curseur ou position fixe avec capture

### Mode Script/Macro
- Enregistrement des clics (position + type de bouton)
- Lecture des séquences enregistrées
- Délai configurable entre chaque clic
- Boucle infinie ou nombre de répétitions défini
- Sauvegarde/chargement des scripts en JSON

### Raccourcis Clavier
| Touche | Action |
|--------|--------|
| F6 | Démarrer/Arrêter le clic simple |
| F7 | Démarrer/Arrêter l'enregistrement |
| F8 | Démarrer/Arrêter la lecture du script |
| Escape | Arrêt d'urgence (tout stopper) |

*Les raccourcis sont personnalisables via les paramètres*

### Autres Fonctionnalités
- Interface moderne avec thème sombre
- Sauvegarde automatique des paramètres et du dernier script
- Instance unique (relancer l'app remet la fenêtre au premier plan)
- Compilation en exécutable (.exe)

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Windows (pour les raccourcis clavier globaux)

### Installation des dépendances

```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

Ou utiliser le script fourni :
```bash
install.bat
```

## Utilisation

### Lancer l'application

```bash
python main.py
```

Ou utiliser le script fourni :
```bash
run.bat
```

### Compiler en .exe

```bash
pyinstaller --onefile --windowed --name AutoClicker main.py
```

Ou utiliser le script fourni :
```bash
build.bat
```

L'exécutable sera créé dans le dossier `dist/`.

## Structure du Projet

```
AutoCliquer/
├── main.py                 # Point d'entrée
├── src/
│   ├── ui/
│   │   ├── app.py          # Fenêtre principale
│   │   ├── simple_clicker.py   # Onglet clic simple
│   │   └── script_recorder.py  # Onglet script/macro
│   ├── core/
│   │   ├── clicker.py      # Logique de clic
│   │   ├── recorder.py     # Enregistrement des clics
│   │   └── hotkeys.py      # Gestion des raccourcis
│   └── utils/
│       ├── config.py       # Configuration persistante
│       └── file_manager.py # Sauvegarde/chargement scripts
├── scripts/                # Dossier pour les scripts sauvegardés
├── requirements.txt
└── build.bat               # Script de compilation
```

## Dépendances

| Package | Description |
|---------|-------------|
| customtkinter | Interface graphique moderne |
| pyautogui | Contrôle de la souris |
| pynput | Écoute globale souris/clavier |
| keyboard | Raccourcis clavier globaux |
| pyinstaller | Compilation en .exe |

## Captures d'écran

### Onglet Clic Simple
Interface permettant de configurer un auto-clic répétitif avec intervalle, type de clic et position personnalisables.

### Onglet Script/Macro
Interface d'enregistrement et de lecture de séquences de clics avec support multi-boutons.

## Sécurité

- **Failsafe** : Déplacez la souris dans un coin de l'écran pour arrêter automatiquement (fonctionnalité pyautogui)
- **Escape** : Appuyez sur Escape à tout moment pour tout arrêter

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

Développé avec l'assistance de Claude (Anthropic).
