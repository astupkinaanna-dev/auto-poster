import os
import requests
from datetime import datetime

# Получаем переменные из GitHub Secrets
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
OR_KEY = os.getenv('OPENROUTER_API_KEY')

def generate_post_text():
    """Генерирует текст поста через OpenRouter (бесплатная модель Qwen 2.5)"""
    today = datetime.now().strftime('%d.%m.%Y')
    
    # Темы меняются в зависимости от дня недели для разнообразия
    topics = [
        "Почему модульный дом выгоднее квартиры зимой",
        "Как мы утепляем дома, чтобы было +22°C в мороз",
        "Терраса зимой: миф или реальность?",
        "Топ-3 ошибки при выборе участка для модульного дома",
        "Как панорамные окна сохраняют тепло",
        "Сколько реально стоит содержание модульного дома в месяц",
        "История одного клиента: переезд из студии в свой дом"
    ]
    topic = topics[datetime.now().weekday() % len(topics)]
    
    prompt = f"""
    Ты — эксперт и контент-менеджер компании KSwooD (модульные дома и бани).
    Сегодня {today}.
    
    Напиши пост для Telegram-канала на тему: "{topic}"
    
    Требования:
    1. Объем: 600-900 знаков (коротко и емко).
    2. Стиль: живой, экспертный, без воды и канцеляризмов.
    3. Структура: цепляющий заголовок, 2-3 абзаца сути, призыв к действию в конце (например, написать нам для расчета).
    4. Используй 2-3 уместных эмодзи. Не используй хештеги в тексте.
    """
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OR_KEY}",
        "HTTP-Referer": "https://github.com", 
        "X-Title": "KSwooD Telegram Bot"
    }
    data = {
        "model": "qwen/qwen-2.5-72b-instruct:free", # Полностью бесплатная мощная модель
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    # Извлекаем текст ответа
    return result['choices'][0]['message']['content'].strip()

def generate_image():
    """Генерирует картинку через Pollinations.ai (без ключей и лимитов)"""
    # Промпт на английском для лучшего качества генерации
    image_prompt = "modern modular barnhouse, winter landscape, snow, warm cozy light from large panoramic windows, wooden facade, cinematic lighting, photorealistic, 8k, architectural photography"
    
    # Кодируем пробелы для URL
    encoded_prompt = requests.utils.quote(image_prompt)
    
    # Формируем ссылку на картинку (размер 1024x1024, без водяных знаков)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={datetime.now().second}"
    
    # Скачиваем картинку
    img_response = requests.get(image_url)
    with open('image.jpg', 'wb') as f:
        f.write(img_response.content)
    
    return 'image.jpg'

def send_to_telegram(text, image_path):
    """Отправляет пост с картинкой в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {
            'chat_id': CHAT_ID,
            'caption': text,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, files=files, data=data)
    
    return response.json()

def main():
    print("Генерация текста...")
    text = generate_post_text()
    print(f"Текст готов: {text[:50]}...")
    
    print("Генерация картинки...")
    image_path = generate_image()
    print("Картинка скачана")
    
    print("Публикация в Telegram...")
    result = send_to_telegram(text, image_path)
    
    if result.get('ok'):
        print("✅ Успешно опубликовано!")
    else:
        print(f"❌ Ошибка Telegram: {result}")

if __name__ == '__main__':
    main()
