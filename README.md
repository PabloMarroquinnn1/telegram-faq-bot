# SmartBot — Telegram FAQ Bot

Sistema de respuestas automatizadas basado en un bot de Telegram, conectado a una API REST desarrollada con FastAPI y PostgreSQL. Incluye un panel administrativo web para gestionar preguntas frecuentes por categorias, con autenticacion JWT y logging de interacciones.

## Tecnologias

| Componente | Tecnologia |
|---|---|
| Bot | Python + python-telegram-bot |
| Backend / API | Python + FastAPI |
| Base de datos | PostgreSQL 15 |
| Panel admin | HTML, CSS, JavaScript |
| Autenticacion | JWT (PyJWT) |
| Contenedores | Docker + Docker Compose |

## Arquitectura

```
┌─────────────────────────────────────┐
│         Usuario Telegram            │
└──────────────┬──────────────────────┘
               │ Telegram API
┌──────────────▼──────────────────────┐
│           Bot Service               │
│           bot/bot.py                │
│  Recibe mensajes, consulta la API,  │
│  responde con la mejor coincidencia │
└──────────────┬──────────────────────┘
               │ HTTP REST
┌──────────────▼──────────────────────┐
│         FastAPI Backend             │
│      backend/app/main.py            │
│  Endpoints: auth, categories,       │
│  questions, config, logs            │
│  Panel admin: templates/index.html  │
└──────────────┬──────────────────────┘
               │ SQLAlchemy
┌──────────────▼──────────────────────┐
│          PostgreSQL 15              │
│  Tablas: categories, questions,     │
│  interaction_logs, config           │
└─────────────────────────────────────┘
```

## Caracteristicas

- **Bot de Telegram:** Responde automaticamente preguntas frecuentes usando coincidencia por palabras clave
- **Panel administrativo:** Interfaz web con autenticacion JWT para gestionar categorias y preguntas
- **Logging:** Registro de todas las interacciones del bot con timestamps
- **Configuracion dinamica:** Mensajes de bienvenida y respuesta por defecto configurables desde el panel
- **Seed automatico:** Carga inicial de categorias y preguntas de ejemplo al iniciar
- **Dockerizado:** Tres servicios orquestados con Docker Compose (db, backend, bot)

## Requisitos

- Docker Desktop 4.x+
- Git

## Instalacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/PabloMarroquinnn1/telegram-faq-bot.git
cd telegram-faq-bot
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales reales (token de Telegram, password de PostgreSQL, etc.).

### 3. Levantar los servicios

```bash
docker-compose up --build
```

El panel administrativo estara disponible en `http://localhost:8000` y el bot comenzara a responder en Telegram.

## Estructura del proyecto

```
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py                # Entry point FastAPI
│       ├── database.py            # Conexion SQLAlchemy + PostgreSQL
│       ├── models/models.py       # Modelos ORM
│       ├── routes/
│       │   ├── auth.py            # Login JWT
│       │   ├── categories.py      # CRUD categorias
│       │   ├── questions.py       # CRUD preguntas
│       │   ├── config.py          # Configuracion dinamica
│       │   └── logs.py            # Consulta de logs
│       ├── services/seed.py       # Datos iniciales
│       └── templates/index.html   # Panel admin
├── bot/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── bot.py                     # Logica del bot de Telegram
├── docker-compose.yml             # Orquestacion de servicios
├── .env.example                   # Template de variables de entorno
└── docs/
    ├── ManualTecnico.md           # Documentacion tecnica
    └── ManualUsuario.md           # Guia de uso
```

## Documentacion

- [Manual Tecnico](docs/ManualTecnico.md) — Arquitectura, modelos, endpoints
- [Manual de Usuario](docs/ManualUsuario.md) — Instalacion y guia paso a paso

## Autor

**Pablo Alejandro Marroquin Cutz**
