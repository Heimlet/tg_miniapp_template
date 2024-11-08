FROM node:16-alpine as build-frontend

WORKDIR /app/frontend

# Copy the environment file for access during the build
COPY .env .env

# Load VITE_ENV variable from the environment
ARG VITE_ENV
ENV VITE_ENV=${VITE_ENV}

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend ./

# Use VITE_ENV to determine the build mode
RUN npm run build -- --mode ${VITE_ENV}

FROM python:3.10-slim as build-backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/backend/django_miniapp

COPY .env .env

COPY backend/django_miniapp/requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY backend/django_miniapp ./

RUN python manage.py collectstatic --noinput

FROM nginx:alpine

COPY --from=build-frontend /app/frontend/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build-backend /app/backend/django_miniapp /app/backend/django_miniapp

COPY --from=build-backend /app/backend/django_miniapp/staticfiles /app/backend/django_miniapp/staticfiles

RUN apk add --no-cache python3 py3-pip postgresql-client
COPY backend/django_miniapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY backend/django_miniapp/entrypoint.sh /app/backend/django_miniapp/entrypoint.sh
RUN chmod +x /app/backend/django_miniapp/entrypoint.sh

WORKDIR /app/backend/django_miniapp

EXPOSE 80

RUN echo ">>> executing entrypoint sh of backend"

ENTRYPOINT ["sh", "/app/backend/django_miniapp/entrypoint.sh"]
