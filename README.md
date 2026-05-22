# Telegram-бот "Таро-справочник"

MVP Telegram-бота для начинающих тарологов. Пользователь выбирает карту из справочника и получает простое толкование по сферам.

## Возможности v1

- справочник всех 78 карт Таро;
- навигация через inline-кнопки;
- старшие и младшие арканы;
- выбор масти для младших арканов;
- толкование: кратко, совет, любовь, работа, финансы;
- эмодзи вместо изображений карт.

## Запуск локально

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
$env:TELEGRAM_BOT_TOKEN="your-token"
python -m tarot_bot.main
```

Опционально можно указать другой путь к контенту:

```powershell
$env:TAROT_CARDS_PATH="data/cards.json"
```

## Тесты

```powershell
python -m unittest discover -s tests
```
