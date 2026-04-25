import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

import math
from django.db.models import Count, Q, Sum, Avg, F


class StatisticsService:

    @staticmethod
    def get_team_statistics(team_id):
        from apps.teams.models import Team
        from apps.matches.models import Match
        team = Team.objects.get(id=team_id)
        matches = Match.objects.filter(
            Q(home_team=team) | Q(away_team=team),
            status='finished'
        )

        stats = {
            'team': team,
            'total_matches': matches.count(),
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_for': 0,
            'goals_against': 0,
        }

        for match in matches:
            if match.home_team == team:
                stats['goals_for'] += match.home_score
                stats['goals_against'] += match.away_score
                if match.home_score > match.away_score:
                    stats['wins'] += 1
                elif match.home_score == match.away_score:
                    stats['draws'] += 1
                else:
                    stats['losses'] += 1
            else:
                stats['goals_for'] += match.away_score
                stats['goals_against'] += match.home_score
                if match.away_score > match.home_score:
                    stats['wins'] += 1
                elif match.away_score == match.home_score:
                    stats['draws'] += 1
                else:
                    stats['losses'] += 1

        if stats['total_matches'] > 0:
            stats['win_rate'] = (stats['wins'] / stats['total_matches']) * 100
            stats['goals_per_match'] = stats['goals_for'] / stats['total_matches']
        else:
            stats['win_rate'] = 0
            stats['goals_per_match'] = 0

        return stats

    @staticmethod
    def get_player_statistics(player_id):
        from apps.players.models import Player
        from apps.matches.models import MatchEvent
        player = Player.objects.get(id=player_id)
        events = MatchEvent.objects.filter(player=player)

        stats = {
            'player': player,
            'total_matches': events.values('match').distinct().count(),
            'goals': events.filter(event_type='goal').count(),
            'assists': events.filter(event_type='assist').count(),
            'shots': events.filter(event_type='shot').count(),
            'passes': events.filter(event_type='pass').count(),
            'fouls': events.filter(event_type='foul').count(),
            'yellow_cards': events.filter(event_type='yellow_card').count(),
            'red_cards': events.filter(event_type='red_card').count(),
            'tackles': events.filter(event_type='tackle').count(),
        }

        if stats['total_matches'] > 0:
            stats['goals_per_match'] = stats['goals'] / stats['total_matches']
            stats['assists_per_match'] = stats['assists'] / stats['total_matches']
        else:
            stats['goals_per_match'] = 0
            stats['assists_per_match'] = 0

        return stats

    @staticmethod
    def get_top_scorers(limit=10, league_id=None, season=None):
        from apps.players.models import Player
        queryset = Player.objects.annotate(
            goals=Count('match_events', filter=Q(match_events__event_type='goal'))
        ).filter(match_events__event_type='goal').order_by('-goals')

        if league_id:
            queryset = queryset.filter(team__league_id=league_id)
        if season:
            queryset = queryset.filter(team__league__season=season)

        return queryset[:limit]

    @staticmethod
    def get_top_assists(limit=10, league_id=None, season=None):
        from apps.players.models import Player
        queryset = Player.objects.annotate(
            assists=Count('match_events', filter=Q(match_events__event_type='assist'))
        ).filter(match_events__event_type='assist').order_by('-assists')

        if league_id:
            queryset = queryset.filter(team__league_id=league_id)
        if season:
            queryset = queryset.filter(team__league__season=season)

        return queryset[:limit]

    @staticmethod
    def get_league_statistics(league_id):
        from apps.leagues.models import League
        from apps.matches.models import Match
        league = League.objects.get(id=league_id)
        matches = Match.objects.filter(league=league, status='finished')

        stats = {
            'league': league,
            'total_matches': matches.count(),
            'total_goals': sum(m.home_score + m.away_score for m in matches),
            'avg_goals_per_match': 0,
            'teams': [],
        }

        if stats['total_matches'] > 0:
            stats['avg_goals_per_match'] = stats['total_goals'] / stats['total_matches']

        for team in league.teams.all():
            team_stats = StatisticsService.get_team_statistics(team.id)
            stats['teams'].append(team_stats)

        stats['teams'] = sorted(stats['teams'], key=lambda x: (
            x['wins'] * 3 + x['draws'],
            x['goals_for'] - x['goals_against']
        ), reverse=True)

        return stats

    @staticmethod
    def get_match_events_summary(match_id):
        from apps.matches.models import Match, MatchEvent
        match = Match.objects.get(id=match_id)
        events = MatchEvent.objects.filter(match=match)

        summary = {
            'match': match,
            'goals': events.filter(event_type='goal').count(),
            'assists': events.filter(event_type='assist').count(),
            'shots': events.filter(event_type='shot').count(),
            'fouls': events.filter(event_type='foul').count(),
            'yellow_cards': events.filter(event_type='yellow_card').count(),
            'red_cards': events.filter(event_type='red_card').count(),
            'tackles': events.filter(event_type='tackle').count(),
            'by_team': {
                match.home_team.name: {
                    'goals': events.filter(team=match.home_team, event_type='goal').count(),
                    'yellow_cards': events.filter(team=match.home_team, event_type='yellow_card').count(),
                    'red_cards': events.filter(team=match.home_team, event_type='red_card').count(),
                },
                match.away_team.name: {
                    'goals': events.filter(team=match.away_team, event_type='goal').count(),
                    'yellow_cards': events.filter(team=match.away_team, event_type='yellow_card').count(),
                    'red_cards': events.filter(team=match.away_team, event_type='red_card').count(),
                }
            }
        }

        return summary

    @staticmethod
    def get_season_statistics(season):
        from apps.matches.models import Match
        from apps.leagues.models import League
        matches = Match.objects.filter(league__season=season, status='finished')

        stats = {
            'season': season,
            'total_matches': matches.count(),
            'total_goals': sum(m.home_score + m.away_score for m in matches),
            'avg_goals_per_match': 0,
            'by_league': [],
        }

        if stats['total_matches'] > 0:
            stats['avg_goals_per_match'] = stats['total_goals'] / stats['total_matches']

        leagues = League.objects.filter(season=season)
        for league in leagues:
            league_stats = StatisticsService.get_league_statistics(league.id)
            stats['by_league'].append(league_stats)

        return stats


class XGModel:

    def predict_xg(self, distance, angle, x_coordinate, y_coordinate):
        return self._calculate_basic_xg(distance, angle)

    def _calculate_basic_xg(self, distance, angle):
        angle_rad = math.radians(angle)
        xg = 1 / (1 + math.exp(-(-1.5 + 0.05 * (45 - distance) + 0.05 * angle_rad)))
        return round(max(0.01, min(0.95, xg)), 4)

    def calculate_distance(self, x, y):
        goal_x, goal_y = 105, 34
        return math.sqrt((goal_x - x) ** 2 + (goal_y - y) ** 2)

    def calculate_angle(self, x, y):
        goal_x, goal_y = 105, 34
        goal_left, goal_right = 30, 38
        angle1 = math.atan2(goal_left - y, goal_x - x)
        angle2 = math.atan2(goal_right - y, goal_x - x)
        return math.degrees(abs(angle1 - angle2))


class XGService:

    @staticmethod
    def calculate_xg_for_shot(shot):
        model = XGModel()
        return model.predict_xg(
            float(shot.distance),
            float(shot.angle),
            float(shot.x_coordinate),
            float(shot.y_coordinate)
        )

    @staticmethod
    def get_player_xg(player_id):
        from apps.events.models import Shot
        shots = Shot.objects.filter(player_id=player_id)
        total_xg = shots.aggregate(total=Sum('xg_value'))['total'] or 0
        goals = shots.filter(is_goal=True).count()
        return {
            'player_id': player_id,
            'total_xg': float(total_xg),
            'actual_goals': goals,
            'xg_difference': float(total_xg) - goals,
            'shots': shots.count()
        }

    @staticmethod
    def get_team_xg(team_id):
        from apps.events.models import Shot
        shots = Shot.objects.filter(team_id=team_id)
        total_xg = shots.aggregate(total=Sum('xg_value'))['total'] or 0
        goals = shots.filter(is_goal=True).count()
        return {
            'team_id': team_id,
            'total_xg': float(total_xg),
            'actual_goals': goals,
            'xg_difference': float(total_xg) - goals,
            'shots': shots.count()
        }

    @staticmethod
    def get_match_xg(match_id):
        from apps.events.models import Shot
        from apps.matches.models import Match
        match = Match.objects.get(id=match_id)
        home_shots = Shot.objects.filter(match_id=match_id, team=match.home_team)
        away_shots = Shot.objects.filter(match_id=match_id, team=match.away_team)
        return {
            'match_id': match_id,
            'home_team': match.home_team.name,
            'away_team': match.away_team.name,
            'home_xg': float(home_shots.aggregate(total=Sum('xg_value'))['total'] or 0),
            'away_xg': float(away_shots.aggregate(total=Sum('xg_value'))['total'] or 0),
            'home_goals': home_shots.filter(is_goal=True).count(),
            'away_goals': away_shots.filter(is_goal=True).count(),
        }

    @staticmethod
    def get_top_xg_players(limit=20):
        from apps.events.models import Shot
        from apps.players.models import Player

        player_stats = Player.objects.annotate(
            total_xg=Sum('shots__xg_value'),
            shots_count=Count('shots'),
            goals_count=Count('shots', filter=Q(shots__is_goal=True))
        ).filter(shots_count__gt=0).order_by('-total_xg')[:limit]

        return [{
            'player': p.name,
            'player_id': p.id,
            'team': p.team.name,
            'total_xg': float(p.total_xg or 0),
            'goals': p.goals_count,
            'shots': p.shots_count,
            'xg_per_shot': float(p.total_xg / p.shots_count if p.shots_count > 0 else 0)
        } for p in player_stats]


class PassNetworkService:

    @staticmethod
    def get_pass_network(match_id, team_id):
        from apps.events.models import Pass
        from apps.players.models import Player

        passes = Pass.objects.filter(match_id=match_id, team_id=team_id, successful=True)

        players = Player.objects.filter(
            Q(id__in=passes.values_list('from_player_id', flat=True)) |
            Q(id__in=passes.values_list('to_player_id', flat=True))
        )

        nodes = []
        for player in players:
            player_passes = passes.filter(
                Q(from_player=player) | Q(to_player=player)
            )
            nodes.append({
                'id': player.id,
                'name': player.name,
                'number': player.number,
                'position': player.position,
                'passes_made': player_passes.filter(from_player=player).count(),
                'passes_received': player_passes.filter(to_player=player).count(),
            })

        edges = []
        pass_counts = passes.values('from_player', 'to_player').annotate(
            count=Count('id')
        ).order_by('-count')

        for pc in pass_counts:
            from_player = Player.objects.get(id=pc['from_player'])
            to_player = Player.objects.get(id=pc['to_player'])
            edges.append({
                'source': pc['from_player'],
                'target': pc['to_player'],
                'source_name': from_player.name,
                'target_name': to_player.name,
                'count': pc['count']
            })

        return {'nodes': nodes, 'edges': edges}


class PoissonPredictionService:

    @staticmethod
    def get_team_attack_strength(team_id, league_id, num_matches=10):
        from apps.matches.models import Match
        from apps.events.models import Shot

        matches = Match.objects.filter(
            Q(home_team_id=team_id) | Q(away_team_id=team_id),
            league_id=league_id,
            status='finished'
        ).order_by('-date')[:num_matches]

        goals_scored = 0
        for match in matches:
            if match.home_team_id == team_id:
                goals_scored += match.home_score
            else:
                goals_scored += match.away_score

        avg_goals = goals_scored / len(matches) if matches else 1.5
        return avg_goals

    @staticmethod
    def get_team_defense_strength(team_id, league_id, num_matches=10):
        from apps.matches.models import Match

        matches = Match.objects.filter(
            Q(home_team_id=team_id) | Q(away_team_id=team_id),
            league_id=league_id,
            status='finished'
        ).order_by('-date')[:num_matches]

        goals_conceded = 0
        for match in matches:
            if match.home_team_id == team_id:
                goals_conceded += match.away_score
            else:
                goals_conceded += match.home_score

        avg_goals = goals_conceded / len(matches) if matches else 1.5
        return avg_goals

    @staticmethod
    def predict_match(home_team_id, away_team_id, league_id):

        home_attack = PoissonPredictionService.get_team_attack_strength(home_team_id, league_id)
        home_defense = PoissonPredictionService.get_team_defense_strength(home_team_id, league_id)
        away_attack = PoissonPredictionService.get_team_attack_strength(away_team_id, league_id)
        away_defense = PoissonPredictionService.get_team_defense_strength(away_team_id, league_id)

        league_avg = 2.5
        home_expected = (home_attack + away_defense) / 2 * league_avg / 2
        away_expected = (away_attack + home_defense) / 2 * league_avg / 2

        home_win_proba = PoissonPredictionService._calculate_poisson_proba(home_expected, away_expected, 'home')
        draw_proba = PoissonPredictionService._calculate_poisson_proba(home_expected, away_expected, 'draw')
        away_win_proba = PoissonPredictionService._calculate_poisson_proba(home_expected, away_expected, 'away')

        return {
            'home_team_id': home_team_id,
            'away_team_id': away_team_id,
            'home_expected_goals': round(home_expected, 2),
            'away_expected_goals': round(away_expected, 2),
            'home_win_probability': round(home_win_proba, 4),
            'draw_probability': round(draw_proba, 4),
            'away_win_probability': round(away_win_proba, 4),
            'predicted_score': f"{round(home_expected)}-{round(away_expected)}"
        }

    @staticmethod
    def _poisson_probability(goals, expected):
        return (math.exp(-expected) * (expected ** goals)) / math.factorial(goals)

    @staticmethod
    def _calculate_poisson_proba(home_exp, away_exp, result):
        if result == 'home':
            probs = [PoissonPredictionService._poisson_probability(h, home_exp) *
                     PoissonPredictionService._poisson_probability(a, away_exp)
                     for h in range(7) for a in range(h)]
            return sum(probs)
        elif result == 'away':
            probs = [PoissonPredictionService._poisson_probability(h, home_exp) *
                     PoissonPredictionService._poisson_probability(a, away_exp)
                     for h in range(7) for a in range(h + 1, 7)]
            return sum(probs)
        else:
            probs = [PoissonPredictionService._poisson_probability(h, home_exp) *
                     PoissonPredictionService._poisson_probability(a, away_exp)
                     for h in range(7) for a in range(7) if h == a]
            return sum(probs)


class PlayerRankingService:

    @staticmethod
    def calculate_impact_score(player_id):
        from apps.events.models import Pass
        from apps.matches.models import MatchEvent

        player_events = MatchEvent.objects.filter(player_id=player_id)
        goals = player_events.filter(event_type='goal').count()
        assists = player_events.filter(event_type='assist').count()
        key_passes = Pass.objects.filter(from_player_id=player_id, is_key_pass=True).count()
        tackles = player_events.filter(event_type='tackle').count()

        impact_score = (goals * 4) + (assists * 3) + (key_passes * 2) + (tackles * 1)

        return {
            'player_id': player_id,
            'goals': goals,
            'assists': assists,
            'key_passes': key_passes,
            'tackles': tackles,
            'impact_score': impact_score
        }

    @staticmethod
    def get_top_players(limit=20, min_matches=3):
        from apps.matches.models import MatchEvent
        from apps.players.models import Player

        players = Player.objects.annotate(
            goals=Count('match_events', filter=Q(match_events__event_type='goal')),
            assists=Count('match_events', filter=Q(match_events__event_type='assist')),
        ).filter(match_events__isnull=False).distinct()

        player_scores = []
        for player in players:
            score = PlayerRankingService.calculate_impact_score(player.id)
            score['player_name'] = player.name
            score['team'] = player.team.name
            score['position'] = player.position
            player_scores.append(score)

        player_scores.sort(key=lambda x: x['impact_score'], reverse=True)
        return player_scores[:limit]


class ScoutingService:

    @staticmethod
    def search_players(
        min_age=None, max_age=None,
        min_goals=None, min_assists=None,
        min_xg=None, min_pass_accuracy=None,
        position=None, league_id=None
    ):
        from apps.players.models import Player
        from apps.events.models import Pass, Shot

        queryset = Player.objects.filter(is_active=True)

        if position:
            queryset = queryset.filter(position=position)
        if league_id:
            queryset = queryset.filter(team__league_id=league_id)

        players_data = []
        for player in queryset:
            stats = PlayerRankingService.calculate_impact_score(player.id)
            player_xg = XGService.get_player_xg(player.id)

            total_passes = Pass.objects.filter(
                Q(from_player=player) | Q(to_player=player)
            ).count()
            successful_passes = Pass.objects.filter(
                Q(from_player=player),
                successful=True
            ).count()
            pass_accuracy = (successful_passes / total_passes * 100) if total_passes > 0 else 0

            if min_xg and player_xg['total_xg'] < min_xg:
                continue
            if min_pass_accuracy and pass_accuracy < min_pass_accuracy:
                continue

            players_data.append({
                'player': player,
                'age': player.age,
                'goals': stats['goals'],
                'assists': stats['assists'],
                'xg': player_xg['total_xg'],
                'pass_accuracy': pass_accuracy,
                'impact_score': stats['impact_score'],
            })

        if min_goals:
            players_data = [p for p in players_data if p['goals'] >= min_goals]
        if min_assists:
            players_data = [p for p in players_data if p['assists'] >= min_assists]
        if min_age:
            players_data = [p for p in players_data if p['age'] and p['age'] >= min_age]
        if max_age:
            players_data = [p for p in players_data if p['age'] and p['age'] <= max_age]

        players_data.sort(key=lambda x: x['impact_score'], reverse=True)
        return players_data


class TeamFormService:

    @staticmethod
    def get_team_form(team_id, num_matches=5):
        from apps.matches.models import Match

        matches = Match.objects.filter(
            Q(home_team_id=team_id) | Q(away_team_id=team_id),
            status='finished'
        ).order_by('-date')[:num_matches]

        form = []
        for match in matches:
            if match.home_team_id == team_id:
                if match.home_score > match.away_score:
                    form.append('W')
                elif match.home_score == match.away_score:
                    form.append('D')
                else:
                    form.append('L')
                goals_for = match.home_score
                goals_against = match.away_score
            else:
                if match.away_score > match.home_score:
                    form.append('W')
                elif match.away_score == match.home_score:
                    form.append('D')
                else:
                    form.append('L')
                goals_for = match.away_score
                goals_against = match.home_score

            form.append({'result': form[-1], 'score': f"{goals_for}-{goals_against}"})

        return {
            'team_id': team_id,
            'form': form,
            'last_5': ''.join([f['result'] for f in form])
        }

    @staticmethod
    def get_league_table(league_id):
        from apps.matches.models import Match
        from apps.teams.models import Team

        teams = Team.objects.filter(league_id=league_id)
        table = []

        for team in teams:
            form_data = TeamFormService.get_team_form(team.id, 5)
            stats = XGService.get_team_xg(team.id)

            matches = Match.objects.filter(
                Q(home_team=team) | Q(away_team=team),
                status='finished'
            )

            wins = draws = losses = goals_for = goals_against = 0
            for match in matches:
                if match.home_team == team:
                    goals_for += match.home_score
                    goals_against += match.away_score
                    if match.home_score > match.away_score:
                        wins += 1
                    elif match.home_score == match.away_score:
                        draws += 1
                    else:
                        losses += 1
                else:
                    goals_for += match.away_score
                    goals_against += match.home_score
                    if match.away_score > match.home_score:
                        wins += 1
                    elif match.away_score == match.home_score:
                        draws += 1
                    else:
                        losses += 1

            table.append({
                'team': team.name,
                'team_id': team.id,
                'played': wins + draws + losses,
                'won': wins,
                'drawn': draws,
                'lost': losses,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'goal_difference': goals_for - goals_against,
                'points': wins * 3 + draws,
                'form': form_data['last_5'],
                'xg': stats['total_xg']
            })

        table.sort(key=lambda x: (x['points'], x['goal_difference'], x['goals_for']), reverse=True)
        for i, team in enumerate(table):
            team['position'] = i + 1

        return table