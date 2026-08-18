import os, requests
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT = os.getenv('TELEGRAM_CHAT_ID')
KEY = os.getenv('OPENROUTER_API_KEY')

print(f"ПРОВЕРКА: Token={'OK' if TOKEN else 'НЕТ'}, Chat={'OK' if CHAT else 'НЕТ'}, Key={'OK' if KEY else 'НЕТ'}")

# Темы по дням недели для разнообразия
topics = {
    0: "Технология ППУ-утепления в модульных домах: почему это лучше минваты и бруса",
    1: "Как панорамные окна сохраняют тепло зимой: мифы и реальность",
    2: "Терраса в модульном доме: как мы увеличиваем полезную площадь в 2 раза",
    3: "Сухая строганная доска vs обычный брус: честное сравнение для будущего владельца",
    4: "Модульный дом vs квартира-студия 35 м²: финансовый разбор за 10 лет",
    5: "Как выбрать участок для модульного дома: 5 критических ошибок",
    6: "История клиента: как семья переехала из городской квартиры в свой дом за 30 дней"
}

today = datetime.now()
weekday = today.weekday()
topic = topics[weekday]
date_str = today.strftime('%d.%m.%Y')

# Детальный промпт в стиле KSwooD
prompt = f"""Ты — главный архитектор и контент-директор компании KSwooD. Мы строим премиальные модульные дома и бани для круглогодичного проживания.

Сегодня {date_str}. Напиши экспертный пост для Telegram-канала на тему:
«{topic}»

СТРОГИЕ ТРЕБОВАНИЯ К ТЕКСТУ:

1. ОБЪЁМ: 1800-2500 знаков. Это не короткая заметка, а полноценный экспертный материал.

2. СТРУКТУРА (обязательна):
   - Цепляющий заголовок (жирным, без эмодзи в заголовке)
   - Вступление-крючок (1-2 предложения, которые цепляют боль или миф клиента)
   - Основная часть: 3-5 конкретных пунктов с цифрами, фактами, сравнениями
   - Личный опыт или кейс KSwooD (можно выдумать правдоподобный)
   - Финал: тёплый, человечный вывод + мягкий призыв к действию

3. СТИЛЬ И ТОН:
   - Экспертный, но тёплый. Как будто архитектор разговаривает с другом за кофе
   - Конкретика: цифры, сроки, цены, сравнения («в 2 раза теплее», «экономия 40 000 ₽ в год»)
   - Без канцеляризмов: никаких «является», «осуществляется», «в целях»
   - Без воды и общих фраз вроде «комфорт и уют»
   - Живые метафоры и образы
   - 3-5 уместных эмодзи (НЕ в каждом предложении!)

4. ФАКТЫ О KSwooD (используй в тексте):
   - Утепление ППУ (пенополиуретан) — в 2 раза эффективнее минваты
   - Каркас из сухой строганной доски камерной сушки
   - Панорамные энергосберегающие стеклопакеты
   - Срок монтажа: 14-30 дней
   - Круглогодичное проживание при -40°C снаружи, +22°C внутри
   - Коммуналка дома 35 м² — около 4000 ₽/мес
   - Собственное производство в России

5. ПРИЗЫВ К ДЕЙСТВИЮ (в конце, мягкий):
   - Не «купите сейчас!»
   - А что-то вроде: «Напишите нам — рассчитаем стоимость вашего проекта за 15 минут» или «Приезжайте на выставочный дом — покажем всё вживую»

6. ЗАПРЕЩЕНО:
   - Хештеги в тексте
   - Восклицательные знаки чаще 2 раз
   - Клише: «лидеры рынка», «индивидуальный подход», «широкий спектр»
   - Обращения «дорогие подписчики», «друзья»

Напиши пост так, чтобы читатель захотел сохранить его и переслать другу."""

# 1. Генерация текста
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {KEY}",
    "HTTP-Referer": "https://github.com",
    "X-Title": "KSwooD Expert Bot"
}

# Используем самую сильную бесплатную модель
models = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.1-8b-instruct:free"
]

text = None
for model in models:
    print(f"Пробуем модель: {model}")
    data = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    r = requests.post(url, headers=headers, json=data)
    j = r.json()
    if r.status_code == 200 and "choices" in j:
        text = j["choices"][0]["message"]["content"].strip()
        print(f"✅ Текст сгенерирован ({len(text)} знаков)")
        break
    print(f"⚠️ {model} не подошла")

if not text:
    text = "🏡 Модульные дома KSwooD — тепло, стиль и свобода. Напишите нам для расчёта."

# 2. Генерация картинки (промпт под тему дня)
image_prompts = {
    0: "cross section of modern modular house wall showing thick polyurethane insulation layers, technical architectural drawing, warm tones, professional",
    1: "modern barnhouse with huge panoramic windows in winter, warm golden light inside, snow outside, cinematic, photorealistic",
    2: "spacious wooden terrace of modular house with cozy outdoor furniture, summer evening, warm string lights, nature view",
    3: "beautiful natural wood texture close-up, dry planed timber, warm tones, architectural detail, professional photography",
    4: "split comparison: left side dark city apartment window view, right side bright modular house with forest view, cinematic",
    5: "beautiful forest plot of land with sun rays, perfect for house construction, morning light, nature photography",
    6: "happy family near modern modular barnhouse, warm evening light, natural lifestyle, cinematic photography"
}

img_prompt = image_prompts.get(weekday, "modern modular barnhouse, architectural photography, cinematic")
img_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(img_prompt)}?width=1024&height=1024&nologo=true&seed={today.second}"
img_data = requests.get(img_url).content
with open("pic.jpg", "wb") as f:
    f.write(img_data)
print("КАРТИНКА: OK ✅")

# 3. Отправка в Telegram
res = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
    files={"photo": open("pic.jpg", "rb")},
    data={"chat_id": CHAT, "caption": text, "parse_mode": "HTML"}
).json()

print("РЕЗУЛЬТАТ:", "УСПЕХ ✅" if res.get("ok") else res)
