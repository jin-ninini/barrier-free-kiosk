import re

from src.menu import HOT_ICE_CATEGORIES


# 한글 수량 표현 (예: "두 잔", "세잔")
KOREAN_NUMBERS = {
    "한": 1, "하나": 1, "두": 2, "둘": 2, "세": 3, "셋": 3, "네": 4, "넷": 4,
    "다섯": 5, "여섯": 6, "일곱": 7, "여덟": 8, "아홉": 9, "열": 10,
}
QUANTITY_PATTERN = re.compile(r"(\d+|" + "|".join(sorted(KOREAN_NUMBERS, key=len, reverse=True)) + r")\s*잔")


# 수량 추출
def extract_quantity(text):
    match = QUANTITY_PATTERN.search(text)
    if match:
        word = match.group(1)
        return int(word) if word.isdigit() else KOREAN_NUMBERS[word]
    return 1


# 온도 추출
def extract_temperature(text):
    if "아이스" in text or "차가운" in text:
        return "아이스"
    elif "핫" in text or "따뜻" in text:
        return "핫"
    return None


def parse_order(text, menu):
    """인식된 문장에서 언급된 음료를 모두 주문으로 변환"""
    quantity = extract_quantity(text)
    temp = extract_temperature(text)
    orders = []
    for category, items in menu.items():
        for drink, price in items.items():
            if drink in text:
                orders.append({
                    "name": drink,
                    "temp": temp if category in HOT_ICE_CATEGORIES else None,
                    "price": price,
                    "quantity": quantity,
                })
    return orders


def describe_order(order):
    """예: '아이스 아메리카노 2잔'"""
    temp = f"{order['temp']} " if order["temp"] else ""
    return f"{temp}{order['name']} {order['quantity']}잔"


def total_price(orders):
    return sum(o["price"] * o["quantity"] for o in orders)
