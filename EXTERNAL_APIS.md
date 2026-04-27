# Configuración de APIs Externas

## Football-Data.org (Recomendado)

### 1. Regístrate gratis
- Ve a: https://www.football-data.org/client/register
- Crea una cuenta gratuita

### 2. Obtén tu API Key
- Copia tu API key del panel

### 3. Configura la variable de entorno
```bash
# Windows
set FOOTBALL_DATA_API_KEY=tu-api-key-aqui

# Linux/Mac
export FOOTBALL_DATA_API_KEY=tu-api-key-aqui
```

O agrega al archivo `.env`:
```
FOOTBALL_DATA_API_KEY=tu-api-key-aqui
```

### 4. Importar datos

```bash
# Premier League
python manage.py import_external --source=football-data --league=PL --limit=20

# La Liga
python manage.py import_external --source=football-data --league=PD --limit=20

# Champions League
python manage.py import_external --source=football-data --league=CL --limit=20
```

## Códigos de Ligas

| Código | Liga |
|--------|------|
| PL | Premier League (Inglaterra) |
| BL1 | Bundesliga (Alemania) |
| PD | La Liga (España) |
| SA | Serie A (Italia) |
| FL1 | Ligue 1 (Francia) |
| CL | Champions League |

## API-Football.com

### 1. Regístrate
- Ve a: https://apifootball.com/
- Suscribe ($9.99/mes)

### 2. Configura
```
API_FOOTBALL_KEY=tu-key
```

## Fútbol Libre (sin API key)

Usa los datos de demo incluidos:
```bash
python manage.py import_matches --demo
```

## Notas

- **Football-Data.org**: 10req/min gratuito - ideal para desarrollo
- **API-Football**: Limitado - mejor para producción
- Los datos se guardan en tu base de datos SQLite/PostgreSQL