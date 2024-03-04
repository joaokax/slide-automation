FROM python:3.11.0rc1
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --system
COPY . .
ENV CONTAINER_NAME mt-presentation
CMD ["echo", "$CONTAINER_NAME"]

