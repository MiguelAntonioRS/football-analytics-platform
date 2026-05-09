# ⚽ Football Analytics Platform
 
Plataforma profesional de análisis de fútbol con Django y Django REST Framework.

## 🚀 Características Completas 

### Gestión de Datos
- [x] Gestión de ligas, equipos y jugadores 
- [x] Registro de partidos y eventos
- [x] Eventos avanzados (tiros y pases)
- [x] Sistema de favoritos

### Análisis Estadístico
- [x] **Expected Goals (xG)**: Modelo predictivo de probabilidades de gol
- [x] **Redes de Pases**: Visualización de conexiones entre jugadores 
- [x] **Predicción Poisson**: Predicción de resultados basada en estadísticas
- [x] **Ranking de Jugadores**: Sistema de impacto score
- [x] **Análisis Táctico**: Heatmaps, formaciones, zonas de juego
- [x] **Tendencias Temporales**: Evolución de equipos y jugadores

### Gamificación (Fase 5) 
- [x] **Fantasy League**: Crea tu equipo fantasy con presupuesto
- [x] **Sistema de Predicciones**: Pronostica resultados de partidos
- [x] **Logros y Badges**: Sistema de recompensas por logros
- [x] **Leaderboards**: Rankings semanales/mensuales/todas lastemps
- [x] **Quizzes**: Trivia de fútbol con puntos

### Comunidad (Fase 6)
- [x] **Blog de Análisis**: Artículos tácticos y estadísticos
- [x] **Chat en Vivo**: Comunidad de usuarios
- [x] **Sistema de Suscripciones**: Planes Free/Basic/Premium

### Autenticación (Fase 1)
- [x] **JWT Authentication**: Registro y login con tokens
- [x] **Perfiles de Usuario**: Información personalizada
- [x] **Notificaciones**: Sistema de alertas

### UX/UI (Fase 4)
- [x] **Dark/Light Mode**: Cambio de tema
- [x] **PWA**: App instalable
- [x] **Responsive Design**: Adaptable a móvil
- [x] **Animaciones**: Transiciones suaves

## 📦 Tecnologías

| Categoría | Tecnología |
|-----------|------------|
| Backend | Django 5+, DRF |
| Auth | JWT (SimpleJWT) |
| Base de datos | SQLite (dev), PostgreSQL (prod) |
| Visualización | Chart.js, Plotly |
| Frontend | HTML5, CSS3, JavaScript |

## 🚀 Instalación

```bash
cd football-analytics-platform

pip install -r requirements.txt

python manage.py migrate

python manage.py import_matches --demo

python manage.py runserver
```

## 🌐 URLs Disponibles

### Páginas
| URL | Descripción |
|-----|-------------|
| `/` | Página principal |
| `/dashboard/` | Dashboard con gráficos |
| `/xg/` | Análisis xG con mapas de calor |
| `/scouting/` | Sistema de scouting |
| `/compare/` | Comparador de jugadores |
| `/tactics/` | Análisis táctico |
| `/trends/` | Tendencias temporales |
| `/fantasy/` | Fantasy League |
| `/blog/` | Blog y comunidad |
| `/admin/` | Panel de administración |

### API Endpoints
| Endpoint | Descripción |
|----------|-------------|
| `POST /api/users/auth/register/` | Registro de usuario |
| `POST /api/users/auth/login/` | Login JWT |
| `GET /api/leagues/` | Lista de ligas |
| `GET /api/teams/` | Lista de equipos |
| `GET /api/players/` | Lista de jugadores |
| `GET /api/matches/` | Lista de partidos |
| `GET /api/events/shots/` | Tiros con xG |
| `GET /api/events/passes/` | Pases entre jugadores |
| `GET /api/analytics/dashboard/` | Datos del dashboard |
| `GET /api/analytics/scorers/` | Top goleadores |
| `GET /api/analytics/xg/` | Estadísticas xG |
| `GET /api/fantasy/predictions/` | Predicciones |
| `GET /api/fantasy/leaderboard/` | Clasificación |
| `GET /api/fantasy/achievements/` | Logros |
| `GET /api/blog/articles/` | Artículos del blog |
| `GET /api/blog/chat/` | Mensajes del chat |

## 🏗 Estructura del Proyecto

```
football-analytics-platform/
├── apps/
│   ├── leagues/      # Gestión de ligas
│   ├── teams/       # Gestión de equipos
│   ├── players/     # Gestión de jugadores
│   ├── matches/     # Partidos y eventos
│   ├── events/       # Tiros y pases
│   ├── analytics/     # Estadísticas y servicios
│   ├── reports/      # Reportes
│   ├── users/        # Usuarios y auth
│   ├── fantasy/       # Fantasy League
│   └── blog/          # Blog y comunidad
├── config/           # Configuración Django
├── static/           # CSS, JS, icons
├── templates/        # Plantillas HTML
└── manage.py
```

## 📊 Modelos Principales

| Modelo | Descripción |
|--------|-------------|
| League | Liga con nombre, país y temporada |
| Team | Equipo con liga, estadio y entrenador |
| Player | Jugador con datos biométricos |
| Match | Partido con marcador |
| MatchEvent | Eventos (gol, asistencia, falta, etc.) |
| Shot | Tiro con coordenadas y xG |
| Pass | Pase entre jugadores |
| Prediction | Predicción de resultado |
| Achievement | Logro desbloqueable |

## 📈 Comandos de Gestión

```bash
# Cargar datos de prueba
python manage.py import_matches --demo

# Calcular valores de mercado
python manage.py calculate_values

# Crear superusuario
python manage.py create_superuser
```

## 🎯 Roadmap Completado

- [x] Fase 1: Autenticación y Usuarios
- [x] Fase 2: Análisis Avanzado
- [x] Fase 3: Scrapers y APIs
- [x] Fase 4: UX/UI Profesional
- [x] Fase 5: Gamificación
- [x] Fase 6: Blog y Comunidad

## 📝 Licencia

MIT License - Libre para uso comercial y personal.
