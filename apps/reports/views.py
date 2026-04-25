from django.http import JsonResponse
from django.views import View
from django.db.models import Count, Q, Sum, Avg
from apps.matches.models import Match, MatchEvent
from apps.teams.models import Team
from apps.players.models import Player
from apps.leagues.models import League

class TeamComparisonView(View):
    def get(self, request):
        team1_id = request.GET.get('team1')
        team2_id = request.GET.get('team2')

        if not team1_id or not team2_id:
            return JsonResponse({'error': 'Se requieren team1 y team2'}, status=400)

        def get_team_comparison(team_id):
            team = Team.objects.get(id=team_id)
            matches = Match.objects.filter(
                Q(home_team=team) | Q(away_team=team),
                status='finished'
            )

            wins = 0
            draws = 0
            losses = 0
            goals_for = 0
            goals_against = 0

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

            return {
                'team': team.name,
                'team_id': team.id,
                'matches': matches.count(),
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'goal_difference': goals_for - goals_against,
                'points': wins * 3 + draws,
            }

        return JsonResponse({
            'team1': get_team_comparison(team1_id),
            'team2': get_team_comparison(team2_id),
        })

class PlayerComparisonView(View):
    def get(self, request):
        player1_id = request.GET.get('player1')
        player2_id = request.GET.get('player2')

        if not player1_id or not player2_id:
            return JsonResponse({'error': 'Se requieren player1 y player2'}, status=400)

        def get_player_comparison(player_id):
            player = Player.objects.get(id=player_id)
            events = MatchEvent.objects.filter(player=player)

            return {
                'player': player.name,
                'player_id': player.id,
                'team': player.team.name,
                'position': player.position,
                'matches': events.values('match').distinct().count(),
                'goals': events.filter(event_type='goal').count(),
                'assists': events.filter(event_type='assist').count(),
                'shots': events.filter(event_type='shot').count(),
                'fouls': events.filter(event_type='foul').count(),
                'yellow_cards': events.filter(event_type='yellow_card').count(),
                'red_cards': events.filter(event_type='red_card').count(),
            }

        return JsonResponse({
            'player1': get_player_comparison(player1_id),
            'player2': get_player_comparison(player2_id),
        })

class LeagueStandingsView(View):
    def get(self, request, league_id):
        league = League.objects.get(id=league_id)
        teams = league.teams.all()

        standings = []
        for team in teams:
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

            standings.append({
                'team': team.name,
                'team_id': team.id,
                'matches': matches.count(),
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'goal_difference': goals_for - goals_against,
                'points': wins * 3 + draws,
            })

        standings.sort(key=lambda x: (x['points'], x['goal_difference'], x['goals_for']), reverse=True)

        return JsonResponse({
            'league': league.name,
            'season': league.season,
            'standings': standings,
        })

class GoalsByPlayerView(View):
    def get(self, request):
        league_id = request.GET.get('league')
        season = request.GET.get('season')
        limit = int(request.GET.get('limit', 20))

        queryset = Player.objects.annotate(
            total_goals=Count('match_events', filter=Q(match_events__event_type='goal'))
        ).filter(match_events__event_type='goal')

        if league_id:
            queryset = queryset.filter(team__league_id=league_id)
        if season:
            queryset = queryset.filter(team__league__season=season)

        top_scorers = queryset.order_by('-total_goals')[:limit]

        data = [{
            'player': p.name,
            'player_id': p.id,
            'team': p.team.name,
            'goals': p.total_goals,
        } for p in top_scorers]

        return JsonResponse({'top_scorers': data})

class GoalsByTeamView(View):
    def get(self, request):
        league_id = request.GET.get('league')
        season = request.GET.get('season')
        limit = int(request.GET.get('limit', 20))

        queryset = Team.objects.annotate(
            total_goals=Sum(
                Q(Q(home_matches__home_score, when__home_team=F('id')) | Q(away_matches__away_score, when__away_team=F('id')))
            )
        )

        if league_id:
            queryset = queryset.filter(league_id=league_id)
        if season:
            queryset = queryset.filter(league__season=season)

        from django.db.models import F, Q, Value
        from django.db.models.functions import Coalesce

        queryset = Team.objects.annotate(
            total_goals=Coalesce(
                Sum('home_matches__home_score', filter=Q(home_matches__status='finished')) +
                Sum('away_matches__away_score', filter=Q(away_matches__status='finished')),
                0
            )
        )

        if league_id:
            queryset = queryset.filter(league_id=league_id)
        if season:
            queryset = queryset.filter(league__season=season)

        teams = queryset.order_by('-total_goals')[:limit]

        data = [{
            'team': t.name,
            'team_id': t.id,
            'league': t.league.name,
            'goals': t.total_goals,
        } for t in teams]

        return JsonResponse({'team_goals': data})