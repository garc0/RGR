# Телеграм бот для управления логистикой

Этот проект представляет собой телеграм бота, созданного для управления логистикой. Бот предоставляет пользователю возможность находить нужные товары,а также осуществлять запросы на организацию транспорта.

## Установка
1. Клонируйте репозиторий: 
   ```
   git clone https://github.com/garc0/RGR
   ```
2. Установите необходимые зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Получите API ключ для телеграм бота у [@BotFather](https://t.me/BotFather)
4. Вставьте ваш API ключ в файл `bot.py`:
   ```python
   API_KEY = 'YOUR_API_KEY'
   ```

## Использование
1. Запустите бота:
   ```
   python bot.py
   ```
2. Найдите бота в телеграме по имени и начните взаимодействие.

## Функционал
- Отображение дашбордов
- Получение информации о товарах на складе
- Организация транспорта

## Скриншоты
![Пример работы бота](пример.jpg)

## Лицензия
Этот проект лицензирован в соответствии с условиями лицензии [MIT](LICENSE).