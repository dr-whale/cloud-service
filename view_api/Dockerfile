FROM composer AS composer
FROM php:8.1-fpm
COPY --from=composer /usr/bin/composer /usr/bin/composer

WORKDIR /app

RUN apt-get update && apt-get install -y supervisor nginx nano mc htop
RUN mkdir -p /var/log/supervisor
RUN docker-php-ext-install pdo pdo_mysql sockets
COPY /etcconf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY /etcconf/nginx.conf /etc/nginx/conf.d/default.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf && \
    sed -i "s/user www-data;/user root;/" /etc/nginx/nginx.conf 
    #sed -i "s/user = www-data/user = root/" /usr/local/etc/php-fpm.d/www.conf && \
    #sed -i "s/group = www-data/group = root/" /usr/local/etc/php-fpm.d/www.conf

COPY . .

RUN composer install