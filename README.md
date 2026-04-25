# Football Analytics Platform

Plataforma profesional de análisis de fútbol construida con Django y Django REST Framework.

## Características

- Gestión de ligas, equipos y jugadores
- Registro de partidos y eventos
- Estadísticas automáticas (equipos y jugadores)
- Dashboard con visualizaciones Chart.js
- API REST completa
- Panel de administración Django

## Requisitos

- Python 3.10+
- pip

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd football-analytics-platform
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar `.env.example` a `.env` y configurar si es necesario:

```bash
copy .env.example .env
```

Para desarrollo local, SQLite se usa por defecto. Para usar PostgreSQL, descomenta las líneas correspondientes en `.env`.

### 5. Crear la base de datos y aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: http://localhost:8000/

## URLs de la Aplicación

| URL | Descripción |
|-----|-------------|
| http://localhost:8000/ | Página principal con dashboard |
| http://localhost:8000/dashboard/ | Dashboard completo con gráficos |
| http://localhost:8000/admin/ | Panel de administración |
| http://localhost:8000/api/ | Documentación de la API |

## API REST Endpoints

### Ligas
- `GET /api/leagues/` - Listar ligas
- `POST /api/leagues/` - Crear liga
- `GET /api/leagues/{id}/` - Detalle de liga
- `PUT /api/leagues/{id}/` - Actualizar liga
- `DELETE /api/leagues/{id}/` - Eliminar liga

### Equipos
- `GET /api/teams/` - Listar equipos
- `POST /api/teams/` - Crear equipo
- `GET /api/teams/{id}/` - Detalle de equipo

### Jugadores
- `GET /api/players/` - Listar jugadores
- `POST /api/players/` - Crear jugador
- `GET /api/players/{id}/` - Detalle de jugador

### Partidos
- `GET /api/matches/` - Listar partidos
- `POST /api/matches/` - Crear partido
- `GET /api/matches/{id}/` - Detalle de partido

### Eventos
- `GET /api/matches/events/` - Listar eventos
- `POST /api/matches/events/` - Crear evento

### Análisis
- `GET /api/analytics/dashboard/` - Datos del dashboard
- `GET /api/analytics/teams/{id}/` - Estadísticas de equipo
- `GET /api/analytics/players/{id}/` - Estadísticas de jugador
- `GET /api/analytics/scorers/` - Top goleadores
- `GET /api/analytics/assists/` - Top asistentes
- `GET /api/analytics/leagues/{id}/` - Estadísticas de liga

### Reportes
- `GET /reports/team-comparison/` - Comparar equipos
- `GET /reports/player-comparison/` - Comparar jugadores
- `GET /reports/standings/{league_id}/` - Tabla de clasificación
- `GET /reports/goals-by-player/` - Goles por jugador
- `GET /reports/goals-by-team/` - Goles por equipo

## Tipos de Eventos

| Tipo | Descripción |
|------|-------------|
| goal | Gol |
| assist | Asistencia |
| shot | Tiro |
| pass | Pase |
| foul | Falta |
| yellow_card | Tarjeta Amarilla |
| red_card | Tarjeta Roja |
| tackle | Entrada |

## Posiciones de Jugadores

| Código | Descripción |
|--------|-------------|
| goalkeeper | Portero |
| defender | Defensa |
| midfielder | Centrocampista |
| forward | Delantero |

## Estados de Partido

| Estado | Descripción |
|--------|-------------|
| scheduled | Programado |
| in_progress | En Progreso |
| finished | Finalizado |
| cancelled | Cancelado |

## Base de Datos

### SQLite (Desarrollo local)
Se usa por defecto. No requiere configuración adicional.

### PostgreSQL (Producción)
Configurar las variables de entorno:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=football_analytics
DB_USER=postgres
DB_PASSWORD=tu-contraseña
DB_HOST=localhost
DB_PORT=5432
```

## Estructura del Proyecto

```
football-analytics-platform/
├── apps/
│   ├── leagues/      # Gestión de ligas
│   ├── teams/        # Gestión de equipos
│   ├── players/      # Gestión de jugadores
│   ├── matches/      # Gestión de partidos y eventos
│   ├── analytics/    # Estadísticas y análisis
│   └── reports/      # Reportes y comparaciones
├── config/           # Configuración del proyecto
├── static/           # Archivos estáticos (CSS, JS)
├── templates/        # Plantillas HTML
├── manage.py         # Script de gestión Django
├── requirements.txt  # Dependencias Python
└── README.md         # Este archivo
```

## Ejemplo de Uso de la API

### Crear una Liga
```bash
curl -X POST http://localhost:8000/api/leagues/ \
  -H "Content-Type: application/json" \
  -d '{"name": "La Liga", "country": "España", "season": "2024-2025"}'
```

### Crear un Equipo
```bash
curl -X POST http://localhost:8000/api/teams/ \
  -H "Content-Type: application/json" \
  -d '{"name": "FC Barcelona", "league": 1, "stadium": "Camp Nou", "coach": "Xavi Hernandez"}'
```

### Crear un Jugador
```bash
curl -X POST http://localhost:8000/api/players/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Robert Lewandowski", "team": 1, "position": "forward", "nationality": "Polonia", "number": 9}'
```

### Crear un Partido
```bash
curl -X POST http://localhost:8000/api/matches/ \
  -H "Content-Type: application/json" \
  -d '{"league": 1, "home_team": 1, "away_team": 2, "date": "2024-09-15T20:00:00Z"}'
```

### Registrar un Gol
```bash
curl -X POST http://localhost:8000/api/matches/events/ \
  -H "Content-Type: application/json" \
  -d '{"match": 1, "minute": 23, "event_type": "goal", "player": 1, "team": 1}'
```

## Panel de Administración

Accede a http://localhost:8000/admin/ con tu superusuario para:

- Gestionar ligas, equipos y jugadores
- Registrar partidos y eventos
- Ver estadísticas básicas
- Administrar usuarios y permisos

## Tecnologías

- **Backend**: Django 4.2, Django REST Framework
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualización**: Chart.js 4.4
- **UI Framework**: Bootstrap 5.3

## Licencia

Este proyecto es software libre y puede ser utilizado para cualquier propósito.