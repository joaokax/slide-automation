FROM python:3.11.0rc1
WORKDIR /app
COPY . .
RUN pip install pipenv && pipenv install --system --deploy && pipenv shell
CMD ["python", "discord-bot.py"]
