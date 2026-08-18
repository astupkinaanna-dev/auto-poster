import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
OR_KEY = os.getenv('OPENROUTER_API_KEY')

print("=" * 50)
print("ПРОВЕРКА ПЕРЕМЕННЫХ:")
print(f"TELEGRAM_BOT_TOKEN: {'✅ есть' if BOT_TOKEN else '❌ ПУСТОЙ!'}")
print(f"TELEGRAM_CHAT_ID: {'✅ есть' if CHAT_ID else '❌ ПУСТОЙ!'}")
print(f"OPENROUTER_API_KEY: {'✅ есть' if OR_KEY else '❌ ПУСТОЙ!'}")
print("=" * 50)

def generate_post_text():
    if not OR_KEY:
        return "⚠️ OPENROUTER_API_KEY не настроен!"
    
    today = datetime.now().strftime('%d.%m.%Y')
    topics = [
        "Почему модульный дом выгоднее квартиры зимой",
        "Как мы утепляем дома, чтобы было +22°C в мороз",
        "Терраса зимой: миф или реальность?",
        "Топ-3 ошибки при выборе участка для модульного дома",
        "Как панорамные окна сохраняют тепло",
        "Сколько реально стоит содержание модульного дома",
        "История клиента: переезд из студии в свой дом"
    ]
    topic = topics[datetime.now().weekday() % len(topics)]
    
    prompt = f"Ты — эксперт компании KSwooD (модульные дома и бани). Напиши пост для Telegram на тему: '{topic}'. Объем 600-800 знаков. Стиль живой, экспертный, без воды. Добавь 2-3 эмодзи. В конце призыв написать нам для расчета."
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OR_KEY}",
        "HTTP-Referer": "https://github.com",
        "X-Title": "KSwooD Bot"
    }
    
    # Пробуем несколько бесплатных моделей по очереди (на случай, если одна недоступна)
    models_to_try = [
        "meta-llama/llama-3.3-70b-instruct:free",
        "google/gemma-3-27b-it:free",
        "mistralai/mistral-small-3.1-24b-instruct:free",
        "qwen/qwen-2.5-72b-instruct"
    ]
    
    for model in models_to_try:
        print(f"Пробуем модель: {model}")
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        
        if response.status_code == 200 and 'choices' in response_data:
            print(f"✅ Модель {model} сработала!")
            return response_data['choices'][0]['message']['content'].strip()
        else:
            print(f"⚠️ Модель {model} не подошла: {response_data.get('error', {}).get('message', 'неизвестная ошибка')}")
            continue
    
    return "⚠️ Не удалось сгенерировать текст. Проверьте API ключ."

def generate_image():
    image_prompt = "modern modular barnhouse, winter landscape, snow, warm cozy light from large panoramic windows, wooden facade, cinematic lighting, photorealistic, 8k"
    encoded_prompt = requests.utils.quote(image_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={datetime.now().second}"
    
    img_response = requests.get(image_url)
    with open('image.jpg', 'wb') as f:
        f.write(img_response.content)
    return 'image.jpg'

def send_to_telegram(text, image_path):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не настроены!")
        return {'ok': False}
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': CHAT_ID, 'caption': text, 'parse_mode': 'HTML'}
        return requests.post(url, files=files, data=data).json()

def main():
    print("Генерация текста...")
    text = generate_post_text()
    print(f"Текст готов: {text[:50]}...")
    
    print("Генерация картинки...")
    image_path = generate_image()
    print("Картинка скачана.")
    
    print("Публикация...")
    result = send_to_telegram(text, image_path)
    
    if result.get('ok'):
        print("✅ Успешно опубликовано!")
    else:
        print(f"❌ Ошибка Telegram: {result}")

if __name__ == '__main__':
    main()
