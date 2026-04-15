# VoiceControl

Простий локальний voice stack для Home Assistant:

- `whisper.cpp` для розпізнавання мовлення (STT)
- `piper` для синтезу мовлення (TTS)
- `FastAPI` сервіс, який приймає аудіо, обробляє команду і повертає озвучену відповідь

## Структура

- `docker-compose.yml` — запуск усіх сервісів
- `app/main.py` — API `/voice`
- `models/` — моделі для Whisper і Piper

## Швидкий старт

```bash
docker compose up -d
```

## Перевірка

1. Перевірка, що контейнери працюють:

```bash
docker compose ps
```

2. Перегляд логів:

```bash
docker compose logs -f whisper piper assistant
```

## API

`POST /voice` (multipart/form-data)

- поле: `file` (аудіофайл)
- відповідь: `audio/wav`

## Далі

- Підключити endpoint до Home Assistant Assist pipeline
- Додати wake word (наприклад, openWakeWord)
- Замінити тестову логіку `handle_command()` на виклики Home Assistant API
