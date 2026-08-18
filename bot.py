import os, requests

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT = os.getenv('TELEGRAM_CHAT_ID')
KEY = os.getenv('OPENROUTER_API_KEY')

print(f"ПРОВЕРКА: Token={'OK' if TOKEN else 'НЕТ'}, Chat={CHAT}, Key={'OK' if KEY else 'НЕТ'}")

# 1. Генерация текста (используем стабильную бесплатную модель)
r = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {KEY}", "HTTP-Referer": "https://github.com"},
    json={
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [{"role": "user", "content": "Короткий пост для Telegram (400 знаков) про преимущества модульных домов KSwooD зимой. Живой стиль, 2 эмодзи, призыв к действию в конце."}]
    }
)
j = r.json()
text = j.get("choices", [{}])[0].get("message", {}).get("content", "Ошибка генерации текста")
print("ТЕКСТ:", text[:60])

# 2. Генерация картинки
img_url = "https://image.pollinations.ai/prompt/modern%20modular%20barnhouse%20winter%20snow%20warm%20light%20panoramic%20windows?width=1024&height=1024&nologo=true"
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

print("РЕЗУЛЬТАТ:", "УСПЕХ ✅" if res.get("ok") else res)
