from django.core.management.base import BaseCommand
from django.utils import timezone
import requests
import os


class Command(BaseCommand):
    help = 'Import data from external football APIs'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=str, default='demo', help='Data source: football-data, api-football, demo')
        parser.add_argument('--league', type=str, default='PL', help='League code (PL, CL, BL1, etc.)')
        parser.add_argument('--limit', type=int, default=10, help='Number of matches to import')

    def handle(self, *args, **options):
        source = options['source']
        league_code = options['league']
        limit = options['limit']

        if source == 'demo':
            print('Use: python manage.py import_matches --demo')
            return

        if source == 'football-data':
            self.connect_football_data(league_code, limit)
        elif source == 'api-football':
            self.connect_api_football(league_code, limit)
        else:
            print(f'Unknown source: {source}')

    def connect_football_data(self, league_code, limit):
        api_key = os.getenv('FOOTBALL_DATA_API_KEY')
        if not api_key:
            print('ERROR: FOOTBALL_DATA_API_KEY not found. Set it in .env file')
            print('Get free key at: https://www.football-data.org/client/register')
            return

        league_mapping = {
            'PL': 'Premier League',
            'BL1': 'Bundesliga',
            'PD': 'La Liga',
            'SA': 'Serie A',
            'FL1': 'Ligue 1',
            'CL': 'Champions League'
        }

        league_name = league_mapping.get(league_code, 'Premier League')
        print(f'Fetching {league_name}...')

        headers = {'X-Auth-Token': api_key}
        url = f'https://api.football-data.org/v4/competitions/{league_code}/matches'

        try:
            response = requests.get(url, headers=headers, params={'limit': limit})
            response.raise_for_status()
            data = response.json()

            matches_data = data.get('matches', [])
            print(f'Found {len(matches_data)} matches')

            from apps.leagues.models import League
            from apps.teams.models import Team
            from apps.matches.models import Match

            league, _ = League.objects.get_or_create(
                name=league_name,
                defaults={'country': 'International', 'season': '2024/2025'}
            )

            count = 0
            for match_data in matches_data[:limit]:
                home_team_data = match_data.get('homeTeam', {})
                away_team_data = match_data.get('awayTeam', {})

                home_team, _ = Team.objects.get_or_create(
                    name=home_team_data.get('name', 'Unknown'),
                    defaults={
                        'league': league,
                        'stadium': home_team_data.get('venue', 'Unknown'),
                        'coach': 'TBD'
                    }
                )

                away_team, _ = Team.objects.get_or_create(
                    name=away_team_data.get('name', 'Unknown'),
                    defaults={
                        'league': league,
                        'stadium': away_team_data.get('venue', 'Unknown'),
                        'coach': 'TBD'
                    }
                )

                utc_date = match_data.get('utcDate')
                match_date = timezone.datetime.fromisoformat(utc_date.replace('Z', '+00:00'))

                score = match_data.get('score', {})
                full_home = score.get('fullTime', {}).get('home') or 0
                full_away = score.get('fullTime', {}).get('away') or 0

                status = match_data.get('status', 'SCHEDULED')
                if status == 'FINISHED':
                    status = 'finished'
                elif status == 'IN_PLAY':
                    status = 'in_progress'
                else:
                    status = 'scheduled'

                match, created = Match.objects.get_or_create(
                    league=league,
                    home_team=home_team,
                    away_team=away_team,
                    date=match_date,
                    defaults={
                        'home_score': full_home,
                        'away_score': full_away,
                        'status': status,
                        'stadium': home_team_data.get('venue', 'Unknown')
                    }
                )

                if created:
                    print(f'+ {home_team.name} {full_home}-{full_away} {away_team.name}')
                    count += 1

            print(f'[OK] Imported {count} matches from {league_name}')
            print(f'Total matches in database: {Match.objects.count()}')

        except requests.exceptions.RequestException as e:
            print(f'API Error: {e}')

    def connect_api_football(self, league_code, limit):
        api_key = os.getenv('API_FOOTBALL_KEY')
        if not api_key:
            print('API_FOOTBALL_KEY not found. Set it in .env')
            return

        print('API-Football integration coming soon')