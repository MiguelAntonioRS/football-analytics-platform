from django.core.management.base import BaseCommand
from django.utils import timezone
import requests
import time


class Command(BaseCommand):
    help = 'Import sample match data from external sources'

    def add_arguments(self, parser):
        parser.add_argument('--demo', action='store_true', help='Load demo data only')

    def handle(self, *args, **options):
        if options['demo']:
            self.load_demo_data()
        else:
            self.stdout.write('Use --demo to load sample data')
            self.stdout.write('For real data, configure API keys in settings')

    def load_demo_data(self):
        from apps.leagues.models import League
        from apps.teams.models import Team
        from apps.players.models import Player
        from apps.matches.models import Match, MatchEvent
        from apps.events.models import Shot, Pass

        if League.objects.exists():
            self.stdout.write('Data already exists. Skipping...')
            return

        self.stdout.write('Loading demo data...')

        la_liga = League.objects.create(
            name='La Liga EA Sports',
            country='España',
            season='2024-2025'
        )

        teams_data = [
            {'name': 'FC Barcelona', 'league': la_liga, 'stadium': 'Estadi Olímpic', 'coach': 'Hans-Dieter Flick'},
            {'name': 'Real Madrid', 'league': la_liga, 'stadium': 'Santiago Bernabéu', 'coach': 'Carlo Ancelotti'},
            {'name': 'Atlético Madrid', 'league': la_liga, 'stadium': 'Civitas Metropolitano', 'coach': 'Diego Simeone'},
            {'name': 'Girona FC', 'league': la_liga, 'stadium': 'Montilivi', 'coach': 'Míchel'},
        ]

        teams = []
        for t in teams_data:
            team = Team.objects.create(**t)
            teams.append(team)
            self.stdout.write(f'  ✓ {team.name}')

        players_data = [
            {'name': 'Lamine Yamal', 'team': teams[0], 'position': 'forward', 'nationality': 'España', 'number': 19},
            {'name': 'Pedri', 'team': teams[0], 'position': 'midfielder', 'nationality': 'España', 'number': 8},
            {'name': 'Robert Lewandowski', 'team': teams[0], 'position': 'forward', 'nationality': 'Polonia', 'number': 9},
            {'name': 'Jules Koundé', 'team': teams[0], 'position': 'defender', 'nationality': 'Francia', 'number': 2},
            {'name': 'Marc-André ter Stegen', 'team': teams[0], 'position': 'goalkeeper', 'nationality': 'Alemania', 'number': 1},
            {'name': 'Vinícius Jr', 'team': teams[1], 'position': 'forward', 'nationality': 'Brasil', 'number': 7},
            {'name': 'Jude Bellingham', 'team': teams[1], 'position': 'midfielder', 'nationality': 'Inglaterra', 'number': 5},
            {'name': 'Kylian Mbappé', 'team': teams[1], 'position': 'forward', 'nationality': 'Francia', 'number': 9},
            {'name': 'Éder Militão', 'team': teams[1], 'position': 'defender', 'nationality': 'Brasil', 'number': 3},
            {'name': 'Thibaut Courtois', 'team': teams[1], 'position': 'goalkeeper', 'nationality': 'Bélgica', 'number': 1},
            {'name': 'Antoine Griezmann', 'team': teams[2], 'position': 'forward', 'nationality': 'Francia', 'number': 7},
            {'name': 'Rodrigo De Paul', 'team': teams[2], 'position': 'midfielder', 'nationality': 'Argentina', 'number': 5},
            {'name': 'Cristhian Stuani', 'team': teams[3], 'position': 'forward', 'nationality': 'Uruguay', 'number': 9},
            {'name': 'Portu', 'team': teams[3], 'position': 'forward', 'nationality': 'España', 'number': 10},
        ]

        players = []
        for p in players_data:
            player = Player.objects.create(**p)
            players.append(player)

        match1 = Match.objects.create(
            league=la_liga, home_team=teams[0], away_team=teams[1],
            date=timezone.now(), stadium='Estadi Olímpic',
            home_score=2, away_score=2, status='finished'
        )

        match2 = Match.objects.create(
            league=la_liga, home_team=teams[2], away_team=teams[0],
            date=timezone.now() - timezone.timedelta(days=3),
            stadium='Civitas Metropolitano', home_score=1, away_score=3, status='finished'
        )

        events = [
            {'match': match1, 'minute': 12, 'event_type': 'goal', 'player': players[2], 'team': teams[0]},
            {'match': match1, 'minute': 34, 'event_type': 'goal', 'player': players[6], 'team': teams[1]},
            {'match': match1, 'minute': 56, 'event_type': 'goal', 'player': players[5], 'team': teams[1]},
            {'match': match1, 'minute': 78, 'event_type': 'goal', 'player': players[0], 'team': teams[0]},
            {'match': match1, 'minute': 45, 'event_type': 'assist', 'player': players[1], 'team': teams[0]},
            {'match': match2, 'minute': 23, 'event_type': 'goal', 'player': players[2], 'team': teams[0]},
            {'match': match2, 'minute': 67, 'event_type': 'goal', 'player': players[2], 'team': teams[0]},
        ]

        for e in events:
            MatchEvent.objects.create(**e)

        shots = [
            {'match': match1, 'player': players[2], 'team': teams[0], 'minute': 12, 'x_coordinate': 95, 'y_coordinate': 34, 'distance': 10, 'angle': 45, 'is_goal': True, 'xg_value': 0.35},
            {'match': match1, 'player': players[6], 'team': teams[1], 'minute': 34, 'x_coordinate': 88, 'y_coordinate': 38, 'distance': 18, 'angle': 35, 'is_goal': True, 'xg_value': 0.22},
            {'match': match1, 'player': players[5], 'team': teams[1], 'minute': 56, 'x_coordinate': 90, 'y_coordinate': 40, 'distance': 16, 'angle': 40, 'is_goal': True, 'xg_value': 0.28},
            {'match': match1, 'player': players[0], 'team': teams[0], 'minute': 78, 'x_coordinate': 92, 'y_coordinate': 34, 'distance': 14, 'angle': 50, 'is_goal': True, 'xg_value': 0.42},
        ]

        for s in shots:
            Shot.objects.create(**s)

        passes = [
            {'match': match1, 'from_player': players[1], 'to_player': players[2], 'team': teams[0], 'minute': 44, 'x_start': 30, 'y_start': 34, 'x_end': 95, 'y_end': 34, 'distance': 65, 'is_key_pass': True, 'successful': True, 'assist': True},
            {'match': match1, 'from_player': players[3], 'to_player': players[1], 'team': teams[0], 'minute': 77, 'x_start': 20, 'y_start': 30, 'x_end': 30, 'y_end': 34, 'distance': 12, 'is_key_pass': False, 'successful': True},
        ]

        for p in passes:
            Pass.objects.create(**p)

        self.stdout.write(self.style.SUCCESS('\n✅ Demo data loaded successfully!'))
        self.stdout.write(f'   {League.objects.count()} leagues')
        self.stdout.write(f'   {Team.objects.count()} teams')
        self.stdout.write(f'   {Player.objects.count()} players')
        self.stdout.write(f'   {Match.objects.count()} matches')