from pathlib import Path

# 프로젝트 경로 (실행 위치와 상관없이 동작하도록 파일 기준으로 계산)
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
MENU_PATH = DATA_DIR / "menu_price.xlsx"
IMAGE_DIR = DATA_DIR / "images"
VOICE_ORDER_SCRIPT = ROOT_DIR / "voice_order.py"
