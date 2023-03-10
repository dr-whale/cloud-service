FROM composer AS composer
FROM php:8.1-fpm
COPY --from=composer /usr/bin/composer /usr/bin/composer

WORKDIR /app

ARG DOMAIN_NAME=localhost

RUN apt-get update && apt-get install -y supervisor nginx nano mc htop libmagickwand-dev
RUN mkdir -p /var/log/supervisor
RUN docker-php-ext-install pdo pdo_mysql sockets
RUN mkdir -p /usr/src/php/ext/imagick; \
    curl -fsSL https://github.com/Imagick/imagick/archive/06116aa24b76edaf6b1693198f79e6c295eda8a9.tar.gz | tar xvz -C "/usr/src/php/ext/imagick" --strip 1; \
    docker-php-ext-install imagick;
COPY /etcconf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY /etcconf/nginx.conf /etc/nginx/conf.d/default.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf && \
    sed -i "s/user www-data;/user root;/" /etc/nginx/nginx.conf && \
    sed -i "s/server_name _;/server_name ${DOMAIN_NAME};/" /etc/nginx/conf.d/default.conf
    
COPY . .

RUN composer install

RUN chown -R :www-data /app/web/assets
RUN chmod -R ug+rw /app/web/assets