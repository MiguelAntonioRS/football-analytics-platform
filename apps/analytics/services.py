from django.db.models import Count, Q, Sum, Avg
from apps.matches.models import Match, MatchEvent
from apps.teams.models import Team
from apps.players.models import Player
from apps.leagues.models import League

class StatisticsService:

    @staticmethod
    def get_team_statistics(team_id):
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