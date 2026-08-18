import os
import requests

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
OR_KEY = os.getenv('OPENROUTER_API_KEY')

print(f"TOKEN: {'OK' if BOT_TOKEN else 'EMPTY'}")
print(f"CHAT_ID: {CHAT_ID}")
print(f"KEY: {'OK' if OR_KEY else 'EMPTY'}")

# Генерация текста
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {"Authorization": f"Bearer {OR_KEY}", "HTTP-Referer": "https://github.com"}
data = {
    "model": "meta-llama/llama-3.3-70b-instruct:free",
    "messages": [{"role": "user", "content": "Напиши пост для Telegram (600 знаков) о модульных домах зимой. 2-3 эмодзи."}]
}
r = requests.post(url, headers=headers, json=data)
j = r.json()
text = j["choices"][0]["message"]["content"] if "choices" in j else "Ошибка генерации"
print(f"Text: {text[:50]}")

# Генерация картинки
img_url = "https://image.pollinations.ai/prompt/modern%20barnhouse%20winter%20snow?width=1024&height=1024&nologo=true"
img = requests.get(img_url).content
with open("img.jpg", "wb") as f:
    f.write(img)
print("Image done")

# Отправка в Telegram
tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
with open("img.jpg", "rb") as f:
    r = requests.post(tg_url, files={"photo": f}, data={"chat_id": CHAT_ID, "caption": text})
print(f"Result: {r.json()}")
