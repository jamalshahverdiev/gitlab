FROM python:3.11.1-slim

# Create app directory
WORKDIR /app

# Install app dependencies
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Bundle app source
COPY app.py .

CMD ["pipenv", "run", "python", "app.py"]