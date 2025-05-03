#!/usr/bin/env bash
set -euo pipefail   # Sofort abbrechen bei Fehlern
set -x               # Echo jeder ausgeführten Zeile

echo "▶️ build.sh: gestartet"

# Basis für GitHub Pages
REPO_NAME="/static_site_generator"
echo "▶️ build.sh: REPO_NAME = '$REPO_NAME'"

# 1) Assets kopieren
echo "▶️ build.sh: Kopiere static → docs"
cp -r static/* docs/

# 2) Seiten generieren
echo "▶️ build.sh: Starte Python‑Generator"
python3 src/main.py "$REPO_NAME"

echo "▶️ build.sh: fertig"
