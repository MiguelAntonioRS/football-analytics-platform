from django.core.management.base import BaseCommand
from apps.leagues.models import League
from apps.teams.models import Team
from apps.players.models import Player
from apps.matches.models import Match, MatchEvent
from apps.events.models import Shot, Pass
from django.utils import timezone
import random
from datetime import timedelta


class Command(BaseCommand):
    help = 'Import sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        la_liga = League.objects.create(
            name='La Liga',
            country='España',
            season='2024-2025'
        )
        premier = League.objects.create(
            name='Premier League',
            country='Inglaterra',
            season='2024-2025'
        )

        teams_data = [
            {'name': 'FC Barcelona', 'league': la_liga, 'stadium': 'Camp Nou', 'coach': 'Hansi Flick'},
            {'name': 'Real Madrid', 'league': la_liga, 'stadium': 'Santiago Bernabéu', 'coach': 'Carlo Ancelotti'},
            {'name': 'Atlético Madrid', 'league': la_liga, 'stadium': 'Metropolitano', 'coach': 'Diego Simeone'},
            {'name': 'Manchester City', 'league': premier, 'stadium': 'Etihad Stadium', 'coach': 'Pep Guardiola'},
            {'name': 'Liverpool', 'league': premier, 'stadium': 'Anfield', 'coach': 'Arne Slot'},
            {'name': 'Arsenal', 'league': premier, 'stadium': 'Emirates', 'coach': 'Mikel Arteta'},
        ]

        teams = []
        for t in teams_data:
            team = Team.objects.create(**t)
            teams.append(team)
            self.stdout.write(f'  Created team: {team.name}')

        players_data = [
            {'name': 'Robert Lewandowski', 'team': teams[0], 'position': 'forward', 'nationality': 'Polonia', 'number': 9},
            {'name': 'Pedri', 'team': teams[0], 'position': 'midfielder', 'nationality': 'España', 'number': 8},
            {'name': 'Gavi', 'team': teams[0], 'position': 'midfielder', 'nationality': 'España', 'number': 6},
            {'name': 'Jules Koundé', 'team': teams[0], 'position': 'defender', 'nationality': 'Francia', 'number': 23},
            {'name': 'Marc-Andre ter Stegen', 'team': teams[0], 'position': 'goalkeeper', 'nationality': 'Alemania', 'number': 1},
            {'name': 'Vinícius Jr', 'team': teams[1], 'position': 'forward', 'nationality': 'Brasil', 'number': 7},
            {'name': 'Jude Bellingham', 'team': teams[1], 'position': 'midfielder', 'nationality': 'Inglaterra', 'number': 5},
            {'name': 'Federico Valverde', 'team': teams[1], 'position': 'midfielder', 'nationality': 'Uruguay', 'number': 15},
            {'name': 'Éder Militão', 'team': teams[1], 'position': 'defender', 'nationality': 'Brasil', 'number': 2},
            {'name': 'Thibaut Courtois', 'team': teams[1], 'position': 'goalkeeper', 'nationality': 'Bélgica', 'number': 1},
            {'name': 'Antoine Griezmann', 'team': teams[2], 'position': 'forward', 'nationality': 'Francia', 'number': 7},
            {'name': 'Rodrigo De Paul', 'team': teams[2], 'position': 'midfielder', 'nationality': 'Argentina', 'number': 5},
            {'name': 'Erling Haaland', 'team': teams[3], 'position': 'forward', 'nationality': 'Noruega', 'number': 9},
            {'name': 'Kevin De Bruyne', 'team': teams[3], 'position': 'midfielder', 'nationality': 'Bélgica', 'number': 17},
            {'name': 'Mohamed Salah', 'team': teams[4], 'position': 'forward', 'nationality': 'Egipto', 'number': 11},
            {'name': 'Bukayo Saka', 'team': teams[5], 'position': 'forward', 'nationality': 'Inglaterra', 'number': 7},
        ]

        players = []
        for p in players_data:
            player = Player.objects.create(**p)
            players.append(player)
            self.stdout.write(f'  Created player: {player.name}')

        match1 = Match.objects.create(
            league=la_liga,
            home_team=teams[0],
            away_team=teams[1],
            date=timezone.now() - timedelta(days=7),
            stadium='Camp Nou',
            home_score=3,
            away_score=2,
            status='finished'
        )

        match2 = Match.objects.create(
            league=la_liga,
            home_team=teams[2],
            away_team=teams[0],
            date=timezone.now() - timedelta(days=3),
            stadium='Metropolitano',
            home_score=1,
            away_score=1,
            status='finished'
        )

        match3 = Match.objects.create(
            league=premier,
            home_team=teams[3],
            away_team=teams[4],
            date=timezone.now() - timedelta(days=5),
            stadium='Etihad Stadium',
            home_score=4,
            away_score=2,
            status='finished'
        )

        events_data = [
            {'match': match1, 'minute': 23, 'event_type': 'goal', 'player': players[0], 'team': teams[0]},
            {'match': match1, 'minute': 35, 'event_type': 'goal', 'player': players[5], 'team': teams[1]},
            {'match': match1, 'minute': 45, 'event_type': 'goal', 'player': players[0], 'team': teams[0]},
            {'match': match1, 'minute': 67, 'event_type': 'assist', 'player': players[1], 'team': teams[0]},
            {'match': match1, 'minute': 68, 'event_type': 'goal', 'player': players[0], 'team': teams[0]},
            {'match': match1, 'minute': 78, 'event_type': 'goal', 'player': players[6], 'team': teams[1]},
            {'match': match1, 'minute': 82, 'event_type': 'yellow_card', 'player': players[3], 'team': teams[0]},
        ]

        for e in events_data:
            MatchEvent.objects.create(**e)
            self.stdout.write(f'  Created event: {e["event_type"]} at {e["minute"]}\'')

        shots_data = [
            {'match': match1, 'player': players[0], 'team': teams[0], 'minute': 23, 'x_coordinate': 95, 'y_coordinate': 34, 'distance': 12, 'angle': 45, 'is_goal': True, 'xg_value': 0.35},
            {'match': match1, 'player': players[0], 'team': teams[0], 'minute': 45, 'x_coordinate': 98, 'y_coordinate': 32, 'distance': 8, 'angle': 55, 'is_goal': True, 'xg_value': 0.55},
            {'match': match1, 'player': players[5], 'team': teams[1], 'minute': 35, 'x_coordinate': 92, 'y_coordinate': 38, 'distance': 15, 'angle': 35, 'is_goal': True, 'xg_value': 0.25},
            {'match': match1, 'player': players[6], 'team': teams[1], 'minute': 78, 'x_coordinate': 88, 'y_coordinate': 40, 'distance': 18, 'angle': 30, 'is_goal': True, 'xg_value': 0.18},
            {'match': match3, 'player': players[12], 'team': teams[3], 'minute': 12, 'x_coordinate': 96, 'y_coordinate': 34, 'distance': 10, 'angle': 50, 'is_goal': True, 'xg_value': 0.42},
            {'match': match3, 'player': players[12], 'team': teams[3], 'minute': 34, 'x_coordinate': 94, 'y_coordinate': 30, 'distance': 12, 'angle': 48, 'is_goal': True, 'xg_value': 0.38},
            {'match': match3, 'player': players[14], 'team': teams[4], 'minute': 56, 'x_coordinate': 90, 'y_coordinate': 36, 'distance': 16, 'angle': 40, 'is_goal': True, 'xg_value': 0.22},
        ]

        for s in shots_data:
            Shot.objects.create(**s)
            self.stdout.write(f'  Created shot at {s["minute"]}\'')

        passes_data = [
            {'match': match1, 'from_player': players[1], 'to_player': players[0], 'team': teams[0], 'minute': 67, 'x_start': 50, 'y_start': 34, 'x_end': 95, 'y_end': 34, 'distance': 45, 'is_key_pass': True, 'successful': True, 'assist': True},
            {'match': match1, 'from_player': players[2], 'to_player': players[1], 'team': teams[0], 'minute': 65, 'x_start': 30, 'y_start': 34, 'x_end': 50, 'y_end': 34, 'distance': 20, 'is_key_pass': False, 'successful': True},
            {'match': match1, 'from_player': players[6], 'to_player': players[5], 'team': teams[1], 'minute': 77, 'x_start': 60, 'y_start': 34, 'x_end': 92, 'y_end': 38, 'distance': 35, 'is_key_pass': True, 'successful': True},
        ]

        for p in passes_data:
            Pass.objects.create(**p)
            self.stdout.write(f'  Created pass')

        self.stdout.write(self.style.SUCCESS('\nSample data imported successfully!'))
        self.stdout.write(f'\n  {League.objects.count()} leagues')
        self.stdout.write(f'  {Team.objects.count()} teams')
        self.stdout.write(f'  {Player.objects.count()} players')
        self.stdout.write(f'  {Match.objects.count()} matches')
        self.stdout.write(f'  {MatchEvent.objects.count()} events')
        self.stdout.write(f'  {Shot.objects.count()} shots')
        self.stdout.write(f'  {Pass.objects.count()} passes')