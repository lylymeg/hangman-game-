# 🪢 Jeu du Pendu Épuré (Hangman Game) — PyQt5

Un jeu de devinette de mots interactif en français, doté d'un rendu vectoriel progressif du bonhomme pendu et d'un clavier virtuel dynamique responsive.

---

## 📸 Aperçu du Jeu

- **Interface épurée & responsive** : Design moderne avec palette pastel/sombre et animations légères.
- **Dessin vectoriel pas à pas** : Rendu graphique dynamique du pendu (gallow & stickman) via `QPainter` à chaque erreur.
- **Double saisie** : Clavier virtuel cliquable à l'écran + gestion native du clavier physique.
- **Mots catégorisés** : Plusieurs banques de mots pour varier le gameplay.

---

## 🚀 Fonctionnalités & Concepts Clés

### 🕹️ Fonctionnalités Principales
- **Banques de mots thématiques** :
  - 💻 **Informatique** (ex: *Algorithme, Base de données, Compilateur*)
  - 🐾 **Animaux** (ex: *Caméléon, Dauphin, Panthère*)
  - 🌍 **Pays** (ex: *Algérie, Norvège, Argentine*)
- **Pendu vectoriel progressif (6 erreurs max)** :
  1. Potence et base
  2. Tête
  3. Tronc
  4. Bras gauche & droit
  5. Jambe gauche
  6. Jambe droite *(Game Over)*
- **Gestion intelligente des touches** : Désactivation visuelle des lettres déjà jouées (avec retour couleur Succès / Échec).
- **Indice & Reset** : Bouton de réinitialisation rapide et masquage automatique des accents.

### 🛠️ Concepts d'Apprentissage (PyQt5 & Python)
- **Dessin vectoriel avancé** : Utilisation de `QPainter`, `QPen`, et `QPainterPath` pour calculer et tracer les segments du pendu étape par étape.
- **Manipulation de chaînes de caractères** : Normalisation Unicode (`unicodedata`) pour gérer les majuscules et la suppression des accents.
- **Grille d'interface dynamique** : Disposition automatique du clavier virtuel avec `QGridLayout` et gestion centralisée des événements de clic.
- **Capture du clavier physique** : Interception globale via `keyPressEvent` avec filtrage des lettres A-Z.

---

## 📋 Prérequis & Installation

### 1. Prérequis
Assurez-vous d'avoir **Python 3.8+** installé sur votre système.

### 2. Installation des Dépendances
Installez PyQt5 via `pip` :

```bash
pip install PyQt5