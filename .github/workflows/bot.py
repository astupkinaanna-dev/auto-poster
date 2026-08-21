import os, requests
from datetime import datetime

print("=" * 60)
print("ВЕРСИЯ 3.0 - НОВЫЙ КОД ЗАПУЩЕН!")
print("=" * 60)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT = os.getenv('TELEGRAM_CHAT_ID')
GROQ_KEY = os.getenv('GROQ_API_KEY')
OWNER_ID = os.getenv('OWNER_ID')

print(f"ПРОВЕРКА: Token={'OK' if TOKEN else 'НЕТ'}, Chat={'OK' if CHAT else 'НЕТ'}, Groq={'OK' if GROQ_KEY else 'НЕТ'}, Owner={'OK' if OWNER_ID else 'НЕТ'}")

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

plan_prompt = f"""Ты — главный архитектор компании KSwooD (модульные дома и бани для круглогодичного проживания).

Сегодня {date_str}. Составь ПОДРОБНЫЙ план экспертной статьи на тему: «{topic}»

План должен включать:
1. Цепляющий заголовок (с цифрой или вопросом)
2. Вступление-крючок (какая боль/миф клиента)
3. 5-6 основных разделов с подзаголовками (каждый — с конкретной цифрой/фактом)
4. Реалистичный кейс клиента KSwooD (имя, ситуация, результат в цифрах)
5. Сравнительная таблица или список «было/стало»
6. Тёплый вывод с мягким призывом

ФАКТЫ О KSwooD:
- Утепление ППУ — в 2 раза эффективнее минваты, служит 50+ лет
- Каркас из сухой строганной доски камерной сушки (влажность 12%)
- Панорамные энергосберегающие стеклопакеты с аргоном
- Монтаж 14-30 дней под ключ
- Круглогодичное проживание: -40°C снаружи, +22°C внутри
- Коммуналка дома 35 м² — ~4000 ₽/мес
- Собственное производство в России
- Гарантия 5 лет на конструктив

Напиши только план, без самого текста."""

def generate_with_groq(prompt, max_tokens):
    models = [
        "llama-3.1-70b-versatile",
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
        "llama-3.1-8b-instant"
    ]
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    for model in models:
        print(f"  Пробуем модель: {model}")
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }
        r = requests.post(url, headers=headers, json=data)
        j = r.json()
        if r.status_code == 200 and "choices" in j:
            print(f"  ✅ Сработала модель: {model}")
            return j["choices"][0]["message"]["content"].strip()
        print(f"  ⚠️ {model}: {j.get('error', {}).get('message', 'неизвестная ошибка')}")
    
    return None

def make_full_post(plan):
    post_prompt = f"""Ты — главный архитектор и контент-директор KSwooD.

Вот план статьи:
{plan}

Напиши ПОЛНЫЙ ТЕКСТ ПОСТА по этому плану.

КРИТИЧЕСКИ ВАЖНО:
- ОБЪЁМ: МИНИМУМ 3500-4500 знаков (это примерно 500-700 слов)
- Каждый раздел плана разворачивай в 2-3 абзаца с конкретикой
- Используй цифры, сравнения, сроки, цены
- Добавь живые детали: «семья Ивановых из Казани», «экономия 47 000 ₽ в год»
- Пиши подзаголовки жирным (через **)
- Используй списки с эмодзи (✅, 📊, 💡, 🔥)
- Стиль: экспертный, но тёплый

ЗАПРЕЩЕНО:
- Писать коротко и общими фразами
- Канцеляризмы, клише, хештеги
- Обращения «друзья», «подписчики»

Призыв в конце: мягкий, «напишите — рассчитаем за 15 минут».

Напиши ВЕСЬ пост целиком, без пояснений."""
    
    return generate_with_groq(post_prompt, 4000)

print("📋 Этап 1: Генерация плана...")
plan = generate_with_groq(plan_prompt, 1500)

if plan:
    print(f"✅ План готов: {len(plan)} знаков")
    print("📝 Этап 2: Разворачиваем в полный пост...")
    text = make_full_post(plan)
    if text:
        print(f"✅ ПОСТ ГОТОВ: {len(text)} знаков")
    else:
        print("❌ Ошибка на этапе 2")
        text = None
else:
    print("❌ ОШИБКА на этапе 1")
    text = None

if not text:
    text = "🏡 Модульные дома KSwooD — тепло, стиль и свобода. Напишите нам для расчёта."

image_prompts = {
    0: "technical cross-section architectural diagram of modern modular house wall showing thick polyurethane foam insulation layers between wooden frame structure, detailed cutaway view, warm natural lighting, professional 3d render, high quality, 8k resolution",
    1: "stunning modern barnhouse with floor-to-ceiling panoramic windows in snowy winter landscape, warm golden light glowing from inside, frost on window edges, cozy atmosphere, cinematic photography, golden hour lighting, architectural digest style, professional quality, 8k",
    2: "spacious wooden deck terrace attached to modern modular barnhouse, cozy outdoor lounge area with plush sofa and coffee table, warm string lights, summer evening sunset, lush green forest in background, lifestyle photography, high quality, 8k",
    3: "extreme close-up of beautiful natural wood texture, dry planed timber with visible grain patterns, warm honey tones, shallow depth of field, professional product photography, studio lighting, high detail, 8k",
    4: "dramatic split-screen comparison: left side dark cramped city apartment with gray view of buildings, right side bright airy modular barnhouse with panoramic forest view, cinematic contrast, professional quality, 8k",
    5: "beautiful forest plot of land with morning sun rays streaming through trees, perfect flat terrain for house construction, dew on grass, magical atmosphere, landscape photography, high quality, 8k",
    6: "happy young family with children standing in front of their new modern modular barnhouse, warm evening golden hour light, natural lifestyle photography, genuine smiles, cinematic quality, 8k"
}

img_prompt = image_prompts.get(weekday, "modern modular barnhouse, architectural photography, cinematic quality, 8k")
img_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(img_prompt)}?width=1280&height=720&nologo=true&seed={today.second}"

print("🎨 Генерация картинки...")
img_data = requests.get(img_url).content
with open("pic.jpg", "wb") as f:
    f.write(img_data)
print(f"✅ КАРТИНКА: OK ({len(img_data)} байт)")

target = OWNER_ID if OWNER_ID else CHAT
prefix = "📝 Пост на модерацию\n\n" if OWNER_ID else ""

print("📤 Отправка картинки...")
res_photo = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
    files={"photo": open("pic.jpg", "rb")},
    data={"chat_id": target, "caption": f"Иллюстрация к посту на тему: {topic}"}
).json()

print("📤 Отправка текста...")
full_text = prefix + text
if OWNER_ID:
    full_text += "\n\n—\n💬 Если всё ок — перешлите оба сообщения в канал."

res_text = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={"chat_id": target, "text": full_text, "parse_mode": "Markdown"}
).json()

if not res_text.get("ok") and "can't parse" in res_text.get("description", "").lower():
    print("⚠️ Markdown ошибка, отправляем без форматирования")
    res_text = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": target, "text": prefix + text}
    ).json()

print("=" * 50)
if res_photo.get("ok") and res_text.get("ok"):
    print("✅ УСПЕХ! Картинка и пост отправлены!")
else:
    print(f"❌ ОШИБКА:")
    print(f"  Фото: {res_photo}")
    print(f"  Текст: {res_text}")
