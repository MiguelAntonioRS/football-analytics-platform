# Football Analytics Platform

Plataforma profesional de análisis de fútbol con Django y Django REST Framework.

## Características

### Gestión de Datos
- **Ligas**: Crear y gestionar ligas con temporadas
- **Equipos**: Registrar equipos con estadísticas
- **Jugadores**: Gestionar jugadores con datos biométricos
- **Partidos**: Registrar partidos y eventos
- **Eventos Avanzados**: Tiros (shots) y pases (passes)

### Análisis Estadístico
- **Expected Goals (xG)**: Modelo predictivo de probabilidades de gol
- **Redes de Pases**: Visualización de conexiones entre jugadores
- **Predicción Poisson**: Predicción de resultados basada en estadísticas
- **Ranking de Jugadores**: Sistema de impacto score
- **Forma de Equipos**: Últimos 5 partidos

### Sistema de Scouting
- Búsqueda avanzada de jugadores
- Filtros por edad, goles, asistencias, xG
- Comparador de jugadores con gráficos radar

### Visualización
- Mapas de tiros con Plotly
- Dashboard con Chart.js
- Comparación con gráficos de barras y radar

## Tecnologías

| Categoría | Tecnología |
|-----------|------------|
| Backend | Django 5+, DRF |
| Base de datos | SQLite / PostgreSQL |
| Análisis | Pandas, NumPy, Scikit-learn |
| Visualización | Chart.js, Plotly |
| Gráfos | NetworkX |

## Instalación

```bash
cd football-analytics-platform

python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py import_sample_data
python manage.py runserver
```

## URLs Disponibles

| URL | Descripción |
|-----|-------------|
| `/` | Página principal |
| `/dashboard/` | Dashboard con gráficos |
| `/admin/` | Panel de administración |
| `/xg/` | Análisis xG |
| `/scouting/` | Sistema de scouting |
| `/compare/` | Comparador de jugadores |
| `/api-docs/` | Documentación API |

## API Endpoints

### Datos Básicos
- `GET /api/leagues/` - Lista de ligas
- `GET /api/teams/` - Lista de equipos
- `GET /api/players/` - Lista de jugadores
- `GET /api/matches/` - Lista de partidos
- `GET /api/events/shots/` - Lista de tiros
- `GET /api/events/passes/` - Lista de pases

### Análisis
- `GET /api/analytics/scorers/` - Top goleadores
- `GET /api/analytics/assists/` - Top asistentes
- `GET /api/analytics/xg/` - Estadísticas xG
- `GET /api/analytics/ranking/` - Ranking de impacto
- `GET /api/analytics/scouting/` - Búsqueda de jugadores
- `GET /api/analytics/pass-network/{match_id}/{team_id}/` - Red de pases

### Reportes
- `GET /reports/team-comparison/` - Comparar equipos
- `GET /reports/player-comparison/` - Comparar jugadores
- `GET /reports/standings/{league_id}/` - Tabla de clasificación

## Modelos Principales

### League
- name, country, season

### Team
- name, league, stadium, coach

### Player
- name, team, position, nationality, age

### Match
- home_team, away_team, date, scores

### MatchEvent
- match, minute, event_type, player, team

### Shot (evento avanzado)
- match, player, coordinates, distance, angle, xg_value

### Pass (evento avanzado)
- from_player, to_player, coordinates, distance, successful

## Comandos de Gestión

```bash
python manage.py import_sample_data
```

## Estructura del Proyecto

```
apps/
├── leagues/      # Gestión de ligas
├── teams/       # Gestión de equipos
├── players/     # Gestión de jugadores
├── matches/     # Partidos y eventos
├── events/      # Tiros y pases
├── analytics/   # Estadísticas y análisis
│   ├── services.py    # Lógica de negocio
│   └── views_advanced.py  # Vistas avanzadas
└── reports/     # Reportes
```

## Expected Goals (xG)

El sistema calcula la probabilidad de gol de cada tiro usando:
- Distancia a portería
- Ángulo del tiro
- Coordenadas en el campo

Fórmula:
```
xG = 1 / (1 + exp(-(-1.5 + 0.05 * (45 - distance) + 0.05 * angle)))
```

## Sistema de Ranking

Score de impacto:
```
impact_score = (goles * 4) + (asistencias * 3) + (pases_clave * 2) + (entradas * 1)
```

## Predicción Poisson

Predice resultados basándose en:
- Fuerza de ataque/defensa de equipos
- Estadísticas históricas de goles
- Distribución de Poisson

## Requisitos

```
Django>=5.0
djangorestframework>=3.14
django-filter>=23.0
numpy>=1.24
pandas>=2.0
scikit-learn>=1.3
networkx>=3.0
matplotlib>=3.7
plotly>=5.18
```