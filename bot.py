import os, requests

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT = os.getenv('TELEGRAM_CHAT_ID')
KEY = os.getenv('OPENROUTER_API_KEY')

print(f"ПРОВЕРКА: Token={'OK' if TOKEN else 'НЕТ'}, Chat={CHAT}, Key={'OK' if KEY else 'НЕТ'}")

# 1. Генерация текста
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {"Authorization": f"Bearer {KEY}", "HTTP-Referer": "https://github.com"}
data = {
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "messages": [{"role": "user", "content": "Короткий пост для Telegram (400 знаков) про преимущества модульных домов KSwooD зимой. Живой стиль, 2 эмодзи, призыв к действию."}]
}
r = requests.post(url, headers=headers, json=data)
j = r.json()

if "choices" in j:
    text = j["choices"][0]["message"]["content"]
    print("ТЕКСТ УСПЕШНО ПОЛУЧЕН")
else:
    print("ОШИБКА OPENROUTER:", j.get("error", j))
    text = "🏡 Модульные дома KSwooD: тепло и уют зимой! Напишите нам для расчёта стоимости."

# 2. Генерация картинки
img_url = "https://image.pollinations.ai/prompt/modern%20modular%20barnhouse%20winter%20snow%20warm%20light?width=1024&height=1024&nologo=true"
img_data = requests.get(img_url).content
with open("pic.jpg", "wb") as f:
    f.write(img_data)
print("КАРТИНКА: OK")

# 3. Отправка в Telegram
res = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
    files={"photo": open("pic.jpg", "rb")},
    data={"chat_id": CHAT, "caption": text}
).json()

print("РЕЗУЛЬТАТ TELEGRAM:", "УСПЕХ ✅" if res.get("ok") else res)
