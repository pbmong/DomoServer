FROM php:8-apache

#RUN a2enmod ssl && a2enmod rewrite
#RUN mkdir -p /etc/apache2/ssl
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

#COPY ./ssl/*.pem /etc/apache2/ssl/
COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./src/ /var/www/html/

EXPOSE 80
EXPOSE 443

#building command: docker build -t domoserver-frontend:latest ./frontend
#container creation:  docker run --name DomoServer-frontend domoserver-frontend:latest 