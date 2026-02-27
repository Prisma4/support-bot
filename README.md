Support Bot
-
___

A Telegram bot using the Django REST API. Designed to receive, process, and respond to support requests.

Used technologies:
- `Django`
- `aiogram` and `aiogram-dialogs`
- `uv`
- `redis`
- `celery`

___
### Quick start

1. Clone the repository

```bash
git clone https://github.com/Prisma4/support-bot.git
cd support-bot
```

2. Create .env file in the root folder and fill it:

```env
DJANGO_SECRET_KEY=django-insecure-...  # your django secret key.
DJANGO_DEBUG=True  # set to False in prod
DJANGO_ALLOWED_HOSTS=backend,localhost  # 'backend' is required, 'localhost' is optional if you want to use Django admin.
PSQL_NAME=todo_list
PSQL_USER=user
PSQL_PASS=some_password
PSQL_PORT=5432
BOT_TOKEN=your_telegram_bot_token  # you can get telegram bot token from @BotFather bot in telegram
BASE_API_URL=http://backend:8000  # base django api url for bot. format: 'container_name:internal_port'
TELEGRAM_BOT_API_TOKEN=some_very_secure_token  # a token used by django to identify that request made by bot
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

#### You can generate `DJANGO_SECRET_KEY` with command bellow ( make sure Django is installed beforehand ):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

3. Run docker-compose

```bash
docker-compose up --build 
```

Now just wait for containers to build, and the bot is ready to use!