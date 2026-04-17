from pathlib import Path

# Absolute paths resolved once, used everywhere
ROOT_DIR = Path(__file__).resolve().parents[3]
SRC_DIR = Path(__file__).resolve().parents[2]
API_DIR = Path(__file__).resolve().parents[1]

FRONTEND_DIR = SRC_DIR / "frontend"
TEMPLATE_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"