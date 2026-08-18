import os
import requests
from datetime import datetime

# ДИАГНОСТИКА: показываем ВСЕ переменные, которые пришли в скрипт
print("=" * 60)
print("ВСЕ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ В СКРИПТЕ:")
for key, value in os.environ.items():
    if any(x in key.upper() for x in ['TELEGRAM', 'OPENROUTER', 'TOKEN', 'KEY', 'CHAT']):
        # Показываем только первые 10 символов для безопасности
        safe_value = value[:10] + '...' if len(value) > 10 else value
        print(f"  {key} = {safe_value}")
print("=" * 60)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
OR_KEY = os.getenv('OPENROUTER_API_KEY')

print(f"\nИтог проверки:")
print(f"  TELEGRAM_BOT_TOKEN: {'✅' if BOT_TOKEN else '❌ ПУСТОЙ'}")
print(f"  TELEGRAM_CHAT_ID: {'✅' if CHAT_ID else '❌ ПУСТОЙ'}")
print(f"  OPENROUTER_API_KEY: {'✅' if OR_KEY else '❌ ПУСТОЙ'}")

def main():
    print("\nСкрипт работает, но секреты не пришли. Проверьте имена в GitHub.")

if __name__ == '__main__':
    main()
   "model": "meta-llama/llama-3.3-70b-instruct:free",
