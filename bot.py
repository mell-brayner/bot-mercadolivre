from playwright.sync_api import sync_playwright
import requests
import time

# =========================
# CONFIGURAÇÕES
# =========================

URL = "https://www.mercadolivre.com.br/pokemon-tcg-ascended-heroes--booster-bundleen/up/MLBU3714719384"

TOKEN = "8505861603:AAEWe9OqwlxqmNSt_hIgDoVGOJ5XH4-DqMI"

CHAT_ID = "1040300203"

# =========================

ultimo_estado = False

def enviar_telegram(msg):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

while True:
    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto(URL, timeout=60000)

            html = page.content().lower()

            disponivel = (
                "comprar agora" in html
                or "adicionar ao carrinho" in html
            )

            if disponivel and not ultimo_estado:

                print("PRODUTO DISPONÍVEL!")

                enviar_telegram(
                    "🚨 Produto voltou ao estoque!"
                )

                ultimo_estado = True

            elif not disponivel:

                print("Sem estoque...")

                ultimo_estado = False

            browser.close()

    except Exception as e:
        print("Erro:", e)

    time.sleep(60)