from src.menu import load_menu
from src.order_parser import describe_order, parse_order, total_price
from src.speech import record_audio, speak, transcribe

END_KEYWORDS = ["종료", "끝", "그만", "결제", "주문 끝", "주문 완료", "다 했어"]
PRICE_KEYWORDS = ["금액", "얼마", "가격"]


# 주문 확인 및 결제 안내
def summarize_order(orders):
    if not orders:
        speak("주문하신 음료가 없습니다.")
        return
    summary = ", ".join(describe_order(o) for o in orders)
    speak(f"{summary} 주문 확인되었습니다. 총 {total_price(orders)}원입니다.")
    speak("카드를 투입해주세요. 결제가 완료되면 음료가 준비됩니다.")


# 금액 요청 처리
def handle_price_request(orders):
    if not orders:
        speak("현재까지 주문하신 음료가 없습니다.")
    else:
        speak(f"현재까지 총 금액은 {total_price(orders)}원입니다.")


def main():
    menu = load_menu()
    orders = []

    speak("안녕하세요. 음료를 주문해주세요. 종료하려면 '종료'라고 말해주세요."
          f" 음료 종류로는 {', '.join(menu)}가 있습니다.")
    while True:
        user_text = transcribe(record_audio())
        print(f"📝 인식된 말: {user_text}")

        if any(x in user_text for x in END_KEYWORDS):
            summarize_order(orders)
            speak("주문이 완료되어 프로그램을 종료합니다. 감사합니다.")
            break

        if any(x in user_text for x in PRICE_KEYWORDS):
            handle_price_request(orders)
            continue

        if "메뉴" in user_text or ("어떤" in user_text and "있어" in user_text):
            for category, items in menu.items():
                speak(f"{category} 카테고리에는 {', '.join(items)}가 있습니다.")
            continue

        for order in parse_order(user_text, menu):
            orders.append(order)
            speak(f"{describe_order(order)} 추가되었습니다.")


if __name__ == "__main__":
    main()
