
REPO_NAME="/static_site_generator"

# 1. Assets kopieren
cp -r static/* docs/

# 2. Seiten generieren
python3 src/main.py "$REPO_NAME"