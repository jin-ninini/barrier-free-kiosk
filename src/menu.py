import pandas as pd

from src.config import MENU_PATH

# 온도(아이스/핫)를 고를 수 있는 카테고리
HOT_ICE_CATEGORIES = ["커피", "차"]


def load_menu():
    """엑셀 가격표를 {카테고리: {메뉴: 가격}} 형태로 불러오기"""
    df = pd.read_excel(MENU_PATH)
    menu = {}
    for _, row in df.iterrows():
        menu.setdefault(row["category"], {})[row["menu"]] = int(row["price"])
    return menu
