FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pipenv

COPY . /app
COPY ./Pipfile /app/
RUN pipenv install --system

EXPOSE 3000
# RUN chown -R www-data:www-data /app
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000”]