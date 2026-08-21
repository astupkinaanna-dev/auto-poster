import os, requests
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT = os.getenv('TELEGRAM_CHAT_ID')
GROQ_KEY = os.getenv('GROQ_API_KEY')

print(f"ПРОВЕРКА: Token={'OK' if TOKEN else 'НЕТ'}, Chat={'OK' if CHAT else 'НЕТ'}, Groq={'OK' if GROQ_KEY else 'НЕТ'}")

# Темы по дням недели
topics = {
    0: "Технология ППУ-утепления в модульных домах: почему это лучше минваты и бруса",
    1: "Как панорамные окна сохраняют тепло зимой: мифы и реальность",
    2: "Терраса в модульном доме: как мы увеличиваем полезную площадь в 2 раза",
    3: "Сухая строганная доска vs обычный брус: честное сравнение",
    4: "Модульный дом vs квартира-студия 35 м²: финансовый разбор за 10 лет",
    5: "Как выбрать участок для модульного дома: 5 критических ошибок",
    6: "История клиента: переезд из городской квартиры в свой дом за 30 дней"
}

today = datetime.now()
weekday = today.weekday()
topic = topics[weekday]
date_str = today.strftime('%d.%m.%Y')

prompt = f"""Ты — главный архитектор компании KSwooD (модульные дома и бани для круглогодичного проживания).

Сегодня {date_str}. Напиши экспертный пост для Telegram на тему: «{topic}»

ТРЕБОВАНИЯ:
- Объём: 1800-2500 знаков
- Структура: цепляющий заголовок (жирным), вступление-крючок, 3-5 пунктов с цифрами и фактами, личный кейс KSwooD, тёплый вывод, мягкий призыв
- Стиль: экспертный, но живой. Как архитектор с другом за кофе
- Конкретика: цифры, сроки, сравнения («в 2 раза теплее», «экономия 40 000 ₽/год»)
- 3-5 эмодзи умеренно
- Без канцеляризмов, клише, хештегов
- Обращений «друзья», «подписчики» — избегать

ФАКТЫ О KSwooD:
- Утепление ППУ — в 2 раза эффективнее минваты
- Каркас из сухой строганной доски
- Панорамные энергосберегающие стеклопакеты
- Монтаж 14-30 дней
- Круглогодичное проживание: -40°C снаружи, +22°C внутри
- Коммуналка дома 35 м² — ~4000 ₽/мес
- Собственное производство в России

Призыв в конце: мягкий, не «купите», а «напишите — рассчитаем за 15 минут» или «приезжайте на выставочный дом».

Напиши пост целиком, без лишних комментариев и пояснений. Только сам текст поста."""

# Генерация текста через Groq
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_KEY}",
    "Content-Type": "application/json"
}
data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7,
    "max_tokens": 2000
}

print("Отправляем запрос в Groq...")
r = requests.post(url, headers=headers, json=data)
j = r.json()

if r.status_code == 200 and "choices" in j:
    text = j["choices"][0]["message"]["content"].strip()
    print(f"✅ ТЕКСТ ПОЛУЧЕН: {len(text)} знаков")
    print(f"ПРЕВЬЮ: {text[:100]}...")
else:
    print(f"❌ ОШИБКА GROQ: {j}")
    text = "🏡 Модульные дома KSwooD — тепло, стиль и свобода. Напишите нам для расчёта."

# Генерация картинки под тему дня
image_prompts = {
    0: "cross section modern house wall thick insulation technical drawing warm tones",
    1: "modern barnhouse huge panoramic windows winter warm light inside snow outside cinematic",
    2: "spacious wooden terrace modular house cozy furniture summer evening warm lights nature",
    3: "beautiful natural wood texture dry timber warm tones architectural detail",
    4: "split comparison dark city apartment window vs bright modular house forest view",
    5: "beautiful forest plot land sun rays morning light nature photography",
    6: "happy family near modern modular barnhouse warm evening light natural lifestyle"
}

img_prompt = image_prompts.get(weekday, "modern modular barnhouse architectural photography")
img_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(img_prompt)}?width=1024&height=1024&nologo=true&seed={today.second}"
img_data = requests.get(img_url).content
with open("pic.jpg", "wb") as f:
    f.write(img_data)
print("КАРТИНКА: OK ✅")

# Отправка в Telegram
res = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
    files={"photo": open("pic.jpg", "rb")},
    data={"chat_id": CHAT, "caption": text}
).json()

print("РЕЗУЛЬТАТ:", "УСПЕХ ✅" if res.get("ok") else res)
