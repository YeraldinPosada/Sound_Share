#Sound Share — Microservices API

> Plataforma de música basada en arquitectura de microservicios. Cada servicio es independiente, con su propia base de datos, y se comunica a través de un API Gateway centralizado.

 **[Ver documentación completa → DOCS.md](./docs/SoundShare_Documentacion_Tecnica.pdf)**

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
Conclusiones
Arquitectura — El patrón de microservicios cumplió su objetivo. Cada servicio se desarrolló, probó y desplegó de forma completamente independiente, y la combinación de tecnologías heterogéneas (Django, Flask, Express, Laravel) no generó fricciones de integración gracias al Gateway como punto de entrada único. La validación cruzada hacia Songs desde los demás servicios mantuvo la integridad referencial de los datos sin generar acoplamiento directo entre ellos.
Rendimiento — El sistema opera de forma estable con hasta ~20 usuarios concurrentes en entorno local, con tiempos de respuesta aceptables. El punto de saturación identificado entre 50 y 60 usuarios es una limitación del hardware de desarrollo, no de la arquitectura. Songs resultó ser el servicio más eficiente bajo carga, lo cual es relevante dado que es consultado por todos los demás. Downloads presentó las latencias más altas incluso en carga baja, producto del overhead combinado de autenticación, validación cruzada y operaciones en PostgreSQL local.
Pruebas — Locust fue efectivo para identificar el límite del entorno. El hallazgo más valioso fue la condición de carrera en operaciones DELETE: los recursos no terminaban de crearse antes de intentar eliminarse. La solución fue introducir un wait_time de 1 a 3 segundos entre tareas, lo que eliminó completamente los fallos. En producción esto se traduciría en la necesidad de manejo de reintentos o colas de mensajes.
Escalabilidad — La arquitectura está diseñada para escalar. Los mismos servicios desplegados en contenedores con balanceo de carga soportarían fácilmente varios cientos de usuarios concurrentes. El siguiente paso natural sería containerizar cada servicio con Docker y orquestarlos con Kubernetes, añadiendo caché (Redis) para las consultas frecuentes al Songs Service.
---

**[Documentación completa → DOCS.md](./docs/SoundShare_Documentacion_Tecnica.pdf)**

