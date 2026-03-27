import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SITE_URL = "https://anidag.ru/api/health"
TG_TOKEN = os.getenv("BOT_TOKEN_HELATH")
TG_CHAT_ID = -5270878964  # твой реальный chat_id

TIMEOUT = 5
STATE_FILE = "site_health_state.txt"  # где храним состояние


def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    r = requests.post(
        url,
        json={"chat_id": TG_CHAT_ID, "text": text},
        timeout=10
    )
    print("TG:", r.status_code, r.text)


def get_previous_state() -> str:
    if not os.path.exists(STATE_FILE):
        return "unknown"
    with open(STATE_FILE, "r") as f:
        return f.read().strip()


def save_state(state: str):
    with open(STATE_FILE, "w") as f:
        f.write(state)


def check_site() -> bool:
    r = requests.get(SITE_URL, timeout=TIMEOUT)
    if r.status_code != 200:
        return False

    # проверяем, что это именно API, а не HTML
    try:
        data = r.json()
    except Exception:
        return False

    return data.get("status") == "ok"


def main():
    prev_state = get_previous_state()

    try:
        is_up = check_site()
    except Exception as e:
        is_up = False
        error_text = str(e)

    if is_up:
        if prev_state != "up":
            send_telegram("✅ API снова доступен")
        save_state("up")
    else:
        if prev_state != "down":
            msg = "❌ API недоступен"
            if "error_text" in locals():
                msg += f"\nОшибка: {error_text}"
            send_telegram(msg)
        save_state("down")


if __name__ == "__main__":
    main()
