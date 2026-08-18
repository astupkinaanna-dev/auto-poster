import os, requests

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT = os.getenv('TELEGRAM_CHAT_ID')
KEY = os.getenv('OPENROUTER_API_KEY')

print(f"ПРОВЕРКА: Token={'OK' if TOKEN else 'НЕТ'}, Chat={'OK' if CHAT else 'НЕТ'}, Key={'OK' if KEY else 'НЕТ'}")

# 1. Генерация текста (используем стабильную бесплатную модель Llama 3.1)
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {"Authorization": f"Bearer {KEY}", "HTTP-Referer": "https://github.com"}
data = {
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "messages": [{"role": "user", "content": "Напиши короткий пост для Telegram (до 500 знаков) про преимущества модульных домов KSwooD зимой. Стиль живой, экспертный, добавь 2-3 эмодзи. В конце призыв написать нам для расчёта стоимости."}]
}
r = requests.post(url, headers=headers, json=data)
j = r.json()

if "choices" in j and len(j["choices"]) > 0:
    text = j["choices"][0]["message"]["content"].strip()
    print("ТЕКСТ: Успешно сгенерирован ✅")
else:
    print("ОШИБКА OPENROUTER:", j.get("error", "Неизвестная ошибка"))
    text = "🏡 Модульные дома KSwooD: тепло, уют и стиль даже зимой! Панорамные окна, современное утепление и быстрый монтаж. Напишите нам для расчёта стоимости вашего идеального дома! ❄️🏠"

# 2. Генерация картинки
print("Генерация картинки...")
img_url = "https://image.pollinations.ai/prompt/modern%20modular%20barnhouse%20winter%20snow%20warm%20light%20panoramic%20windows%20photorealistic?width=1024&height=1024&nologo=true"
img_data = requests.get(img_url).content
with open("pic.jpg", "wb") as f:
    f.write(img_data)
print("КАРТИНКА: OK ✅")

# 3. Отправка в Telegram
print("Отправка в Telegram...")
res = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
    files={"photo": open("pic.jpg", "rb")},
    data={"chat_id": CHAT, "caption": text, "parse_mode": "HTML"}
).json()

if res.get("ok"):
    print("РЕЗУЛЬТАТ: УСПЕХ ✅ Пост опубликован в канале!")
else:
    print("РЕЗУЛЬТАТ: ОШИБКА TELEGRAM ❌", res)
