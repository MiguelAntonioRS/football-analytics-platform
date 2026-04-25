from django.core.management.base import BaseCommand
from apps.players.models import Player
from apps.analytics.services import XGService, PlayerRankingService


class Command(BaseCommand):
    help = 'Calculate market value estimates for players'

    def add_arguments(self, parser):
        parser.add_argument('--player', type=int, help='Specific player ID')
        parser.add_argument('--team', type=int, help='Team ID')
        parser.add_argument('--min-goals', type=int, default=5, help='Minimum goals filter')

    def handle(self, *args, **options):
        if options['player']:
            self.calculate_player_value(options['player'])
        elif options['team']:
            self.calculate_team_values(options['team'])
        else:
            self.calculate_all_values(options['min_goals'])

    def calculate_player_value(self, player_id):
        try:
            player = Player.objects.get(id=player_id)
            value = self.calculate_value(player)
            self.stdout.write(f'{player.name}: €{value:.1f}M')
        except Player.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Player {player_id} not found'))

    def calculate_team_values(self, team_id):
        players = Player.objects.filter(team_id=team_id)
        for player in players:
            value = self.calculate_value(player)
            self.stdout.write(f'{player.name}: €{value:.1f}M')

    def calculate_all_values(self, min_goals):
        self.stdout.write('Calculating market values...\n')
        self.stdout.write('-' * 50)

        players = Player.objects.filter(is_active=True)
        values = []

        for player in players:
            stats = PlayerRankingService.calculate_impact_score(player.id)
            xg_data = XGService.get_player_xg(player.id)

            if stats['goals'] >= min_goals:
                value = self.calculate_value(player)
                values.append((player, value, stats))

        values.sort(key=lambda x: x[1], reverse=True)

        self.stdout.write(f'{"Jugador":<25} {"Equipo":<15} {"Valor":<12} {"Goles":<6} {"xG":<6}')
        self.stdout.write('-' * 70)

        for player, value, stats in values[:20]:
            self.stdout.write(
                f'{player.name:<25} {player.team.name[:14]:<15} '
                f'€{value:>6.1f}M    {stats["goals"]:>4}    {xg_data["total_xg"]:>5.2f}'
            )

        self.stdout.write('-' * 50)
        self.stdout.write(f'Total players analyzed: {len(values)}')

    def calculate_value(self, player):
        stats = PlayerRankingService.calculate_impact_score(player.id)
        xg_data = XGService.get_player_xg(player.id)
        age = player.age or 25

        base_value = 1.0

        impact_score = stats['impact_score']
        if impact_score > 100:
            base_value *= 3.0
        elif impact_score > 50:
            base_value *= 2.0
        elif impact_score > 20:
            base_value *= 1.5

        if stats['goals'] > 20:
            base_value *= 2.5
        elif stats['goals'] > 10:
            base_value *= 1.8
        elif stats['goals'] > 5:
            base_value *= 1.3

        if xg_data['total_xg'] > stats['goals']:
            base_value *= 1.2

        if age < 23:
            base_value *= 1.5
        elif age < 26:
            base_value *= 1.2
        elif age > 30:
            base_value *= 0.7

        position_multipliers = {
            'forward': 1.3,
            'midfielder': 1.1,
            'defender': 0.9,
            'goalkeeper': 0.8
        }
        base_value *= position_multipliers.get(player.position, 1.0)

        return base_value * 10