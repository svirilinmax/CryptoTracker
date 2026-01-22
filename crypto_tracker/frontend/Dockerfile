## frontend/Dockerfile
#FROM nginx:alpine
#
## Копируем все файлы фронтенда в nginx
#COPY frontend/ /usr/share/nginx/html/
#
## Экспозируем порт
#EXPOSE 80



# Если хотите, чтобы при открытии http://localhost:8080 автоматически показывался index.html,
#можете добавить в Dockerfile (опционально):

 #dockerfile
  # frontend/Dockerfile
FROM nginx:alpine

  # Копируем все файлы фронтенда в nginx
# COPY frontend/ /usr/share/nginx/html/
COPY ./html /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

  # Убеждаемся, что index.html является файлом по умолчанию
RUN echo "server { listen 80; root /usr/share/nginx/html; index index.html; location /{ try_files \$uri \$uri/ /index.html; }}" > /etc/nginx/conf.d/default.conf

  # Экспозируем порт
EXPOSE 80
