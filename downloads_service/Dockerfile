FROM php:8.3-fpm

RUN apt-get update && apt-get install -y \
    git \
    curl \
    zip \
    unzip \
    libpng-dev \
    libjpeg-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    libpq-dev \        
    && docker-php-ext-install \
        pdo \
        pdo_pgsql \   
        mbstring \
        zip \
        exif \
        pcntl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ← ELIMINADO: el segundo RUN de pdo_pgsql (era redundante y rompía el build)

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /app

COPY composer.json composer.lock ./
RUN composer install --no-scripts --no-autoloader --prefer-dist

COPY . .
RUN composer dump-autoload --optimize

RUN chown -R www-data:www-data /app/storage /app/bootstrap/cache \
    && chmod -R 775 /app/storage /app/bootstrap/cache

EXPOSE 8001

CMD until php artisan migrate --force; do echo "Esperando PostgreSQL..."; sleep 3; done \
    && php artisan serve --host=0.0.0.0 --port=8001