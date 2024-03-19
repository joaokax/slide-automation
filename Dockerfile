FROM python:3.11.0rc1
WORKDIR /app
COPY .env credentials.json token.json ./
COPY Pipfile Pipfile.lock ./
RUN sudo pip install pipenv && sudo pipenv install --deploy --system
COPY . .
CMD ["sudo", "python", "discord-bot.py"]