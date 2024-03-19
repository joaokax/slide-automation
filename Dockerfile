FROM python:3.11.0rc1
WORKDIR /app
COPY .env ./
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy
COPY . .
CMD ["python", "discord-bot.py"]
