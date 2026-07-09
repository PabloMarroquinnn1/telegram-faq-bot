import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = "http://backend:8000"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

def get_updates(offset=None):
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    res = requests.get(f"{TELEGRAM_API}/getUpdates", params=params, timeout=35)
    return res.json()

def search_answer(query):
    res = requests.get(f"{API_URL}/api/questions/search/query", params={"q": query})
    return res.json()

def log_query(telegram_user, query_text, response_text):
    requests.post(f"{API_URL}/api/logs/", json={
        "telegram_user": telegram_user,
        "query_text": query_text,
        "response_text": response_text
    })

def get_categories():
    res = requests.get(f"{API_URL}/api/categories/")
    return res.json()

def handle_update(update):
    message = update.get("message")
    if not message:
        return

    chat_id = str(message["chat"]["id"])
    text = message.get("text", "")
    user = message.get("from", {})
    username = user.get("username") or user.get("first_name", "Anonimo")

    if text == "/start":
        send_message(chat_id,
            "Bienvenido a SmartBot.\n\n"
            "Puedo responder tus preguntas frecuentes.\n"
            "Escribe tu pregunta y te respondere automaticamente.\n\n"
            "Comandos:\n"
            "/start - Iniciar el bot\n"
            "/help - Ver ayuda\n"
            "/categorias - Ver categorias"
        )
        return

    if text == "/help":
        send_message(chat_id,
            "Escribe tu pregunta directamente en el chat.\n\n"
            "Ejemplos:\n"
            "- Como me inscribo a un curso\n"
            "- Cual es la nota minima para aprobar\n"
            "- Como recupero mi contrasena"
        )
        return

    if text == "/categorias":
        cats = get_categories()
        if cats:
            msg = "Categorias disponibles:\n\n"
            for c in cats:
                msg += f"- {c['name']}: {c.get('description', '')}\n"
            send_message(chat_id, msg)
        else:
            send_message(chat_id, "No hay categorias registradas.")
        return

    data = search_answer(text)
    if data.get("found"):
        answer = data["answer"]
        send_message(chat_id, answer)
    else:
        answer = None
        send_message(chat_id,
            "No encontre una respuesta para tu consulta.\n"
            "Intenta reformular tu pregunta o contacta a soporte."
        )

    log_query(username, text, answer)

def main():
    print("Bot iniciado...")
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                handle_update(update)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()