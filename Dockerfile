FROM python:3.11.0rc1
WORKDIR /app
COPY .env credentials.json token.json ./
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --system
COPY . .
CMD ["python", "discord-bot.py"]
