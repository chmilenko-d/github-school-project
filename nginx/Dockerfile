# Фронтенд собирается локально (npm run build), dist копируется
FROM nginx:alpine
COPY frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
