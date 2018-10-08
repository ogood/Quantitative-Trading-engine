FROM nginx
ADD  site.conf /etc/nginx/conf.d
RUN mkdir -p /file/static
ADD  index.html /file/static

EXPOSE 8000