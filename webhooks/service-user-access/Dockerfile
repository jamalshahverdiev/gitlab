# Use the latest slim image of Python 3.12
FROM python:3.12-slim
WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY app.py .
CMD ["pipenv", "run", "python", "app.py"]