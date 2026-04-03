#Sound Share — Microservices API

> Plataforma de música basada en arquitectura de microservicios. Cada servicio es independiente, con su propia base de datos, y se comunica a través de un API Gateway centralizado.

 **[Ver documentación completa → DOCS.md](./DOCS.md)**

---

## Arquitectura General

```
Cliente
   │
   ▼
API Gateway (Laravel + MySQL) — :8000
   │
   ├──► Songs Service        (Django  + MySQL)       — :8002
   ├──► Playlists Service    (Flask   + Firebase)     — :5000
   ├──► Interactions Service (Express + MongoDB)      — :3000
   ├──► Downloads Service    (Laravel + PostgreSQL)   — :8001
   └──► Lyrics Service       (Flask   + MySQL)        — :5001
```

> Todos los clientes consumen el sistema únicamente a través del **API Gateway** en el puerto `8000`.  
> La comunicación entre microservicios se realiza mediante **APIs REST (HTTP)**.

---

##  Despliegue Rápido

### Requisitos

| Herramienta | Versión mínima |
|-------------|---------------|
| PHP + Composer | >= 8.1 |
| Python + pip | >= 3.10 |
| Node.js + npm | >= 18 |
| MySQL | >= 8.0 |
| PostgreSQL | >= 14 |
| MongoDB | >= 6.0 |
| Firebase | Cuenta con Firestore habilitado |

### Orden de arranque recomendado

```
1. Songs Service     ← todos los demás dependen de este
2. API Gateway
3. Downloads Service
4. Playlists Service
5. Interactions Service
6. Lyrics Service
```

### Comandos rápidos

```bash
# Songs (Django) — Puerto 8002
cd songs && python manage.py runserver 8002

# Gateway (Laravel) — Puerto 8000
cd gateway && php artisan serve

# Downloads (Laravel) — Puerto 8001
cd downloads && php artisan serve --port=8001

# Playlists (Flask) — Puerto 5000
cd playlists && python app.py

# Interactions (Express) — Puerto 3000
cd interactions && node server.js

# Lyrics (Flask) — Puerto 5001
cd lyrics && python app.py
```

> Para instrucciones detalladas de configuración de variables de entorno y base de datos, ver **[DOCS.md → Despliegue](./DOCS.md#despliegue-detallado)**.

---

## Resumen de Endpoints

| Servicio | Método | Ruta | Auth |
|----------|--------|------|:----:|
| Auth | POST | `/api/login` | ❌ |
| Auth | POST | `/api/register` | ❌ |
| Auth | POST | `/api/logout` | ✅ |
| Songs | GET | `/api/songs` | ❌ |
| Songs | POST | `/api/songs` | ❌ |
| Playlists | GET | `/api/playlists` | ✅ |
| Playlists | POST | `/api/playlists` | ✅ |
| Interactions | POST | `/api/likes` | ✅ |
| Interactions | POST | `/api/favorites` | ✅ |
| Downloads | POST | `/api/downloads` | ✅ |
| Lyrics | GET | `/api/lyrics` | ❌ |
| Lyrics | POST | `/api/lyrics` | ❌ |

> Ver tabla completa en **[DOCS.md → Endpoints](./DOCS.md#endpoints-del-api-gateway)**.

---

## Pruebas de Rendimiento (Locust)

| Servicio | Límite estable | Punto de saturación |
|----------|---------------|---------------------|
| Songs | ~50 usuarios | 50–60 usuarios |
| Downloads | ~50 usuarios | 50–60 usuarios |
| Interactions | ~50 usuarios | 50–60 usuarios |
| Playlists | ~50 usuarios | 50–60 usuarios |
| Lyrics | ~50 usuarios | 50–60 usuarios |

> El sistema fue probado en hardware local. El punto de saturación se encuentra entre **50 y 60 usuarios concurrentes**.  
> Ver análisis completo en **[DOCS.md → Pruebas](./DOCS.md#pruebas-de-rendimiento)**.

---

## Estructura del Repositorio

```
sound-share/
├── gateway/          # API Gateway (Laravel + MySQL)
├── songs/            # Microservicio Songs (Django + MySQL)
├── playlists/        # Microservicio Playlists (Flask + Firebase)
├── interactions/     # Microservicio Interactions (Express + MongoDB)
├── downloads/        # Microservicio Downloads (Laravel + PostgreSQL)
├── lyrics/           # Microservicio Lyrics (Flask + MySQL)
├── locust/           # Scripts de pruebas de rendimiento
│   ├── downloads_locust.py
│   ├── interactions_locust.py
│   ├── playlists_locust.py
│   ├── songs_locust.py
│   └── lyrics_locust.py
├── README.md
└── DOCS.md           # Documentación completa
```

---

**[Documentación completa → DOCS.md](./DOCS.md)**
