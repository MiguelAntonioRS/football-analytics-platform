import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from apps.analytics.services import PassNetworkService, XGService, PoissonPredictionService, PlayerRankingService, TeamFormService, ScoutingService


class PassNetworkView(View):
    def get(self, request, match_id, team_id):
        network_data = PassNetworkService.get_pass_network(match_id, team_id)
        return JsonResponse(network_data)


class ShotMapView(View):
    def get(self, request, match_id):
        from apps.events.models import Shot
        shots = Shot.objects.filter(match_id=match_id)
        data = [{
            'x': float(s.x_coordinate),
            'y': float(s.y_coordinate),
            'is_goal': s.is_goal,
            'xg': float(s.xg_value),
            'player': s.player.name,
            'minute': s.minute
        } for s in shots]
        return JsonResponse({'shots': data})


class PredictionView(View):
    def get(self, request, home_team_id, away_team_id, league_id):
        prediction = PoissonPredictionService.predict_match(home_team_id, away_team_id, league_id)
        return JsonResponse(prediction)


class RankingView(View):
    def get(self, request):
        limit = int(request.query_params.get('limit', 20))
        ranking = PlayerRankingService.get_top_players(limit)
        return JsonResponse({'ranking': ranking})


class ScoutingView(View):
    def get(self, request):
        min_age = request.GET.get('min_age')
        max_age = request.GET.get('max_age')
        min_goals = request.GET.get('min_goals')
        min_assists = request.GET.get('min_assists')
        min_xg = request.GET.get('min_xg')
        position = request.GET.get('position')
        league_id = request.GET.get('league')

        players = ScoutingService.search_players(
            min_age=int(min_age) if min_age else None,
            max_age=int(max_age) if max_age else None,
            min_goals=int(min_goals) if min_goals else None,
            min_assists=int(min_assists) if min_assists else None,
            min_xg=float(min_xg) if min_xg else None,
            position=position,
            league_id=int(league_id) if league_id else None
        )

        data = [{
            'player': p['player'].name,
            'player_id': p['player'].id,
            'team': p['player'].team.name,
            'age': p['age'],
            'position': p['player'].position,
            'goals': p['goals'],
            'assists': p['assists'],
            'xg': p['xg'],
            'pass_accuracy': p['pass_accuracy'],
            'impact_score': p['impact_score']
        } for p in players]

        return JsonResponse({'players': data})


class XGAnalysisView(View):
    def get(self, request):
        player_id = request.GET.get('player_id')
        team_id = request.GET.get('team_id')
        match_id = request.GET.get('match_id')

        if player_id:
            data = XGService.get_player_xg(int(player_id))
        elif team_id:
            data = XGService.get_team_xg(int(team_id))
        elif match_id:
            data = XGService.get_match_xg(int(match_id))
        else:
            data = {'top_players': XGService.get_top_xg_players(20)}

        return JsonResponse(data)


class PlayerComparisonView(View):
    def get(self, request):
        player1_id = request.GET.get('player1')
        player2_id = request.GET.get('player2')

        if not player1_id or not player2_id:
            return JsonResponse({'error': 'Se requieren player1 y player2'}, status=400)

        player1_stats = PlayerRankingService.calculate_impact_score(int(player1_id))
        player2_stats = PlayerRankingService.calculate_impact_score(int(player2_id))

        from apps.players.models import Player
        player1 = Player.objects.get(id=int(player1_id))
        player2 = Player.objects.get(id=int(player2_id))

        player1_xg = XGService.get_player_xg(int(player1_id))
        player2_xg = XGService.get_player_xg(int(player2_id))

        return JsonResponse({
            'player1': {
                'name': player1.name,
                'team': player1.team.name,
                'position': player1.position,
                **player1_stats,
                'xg': player1_xg
            },
            'player2': {
                'name': player2.name,
                'team': player2.team.name,
                'position': player2.position,
                **player2_stats,
                'xg': player2_xg
            }
        })


class TeamFormView(View):
    def get(self, request, team_id):
        form_data = TeamFormService.get_team_form(team_id)
        return JsonResponse(form_data)


class LeagueTableView(View):
    def get(self, request, league_id):
        table = TeamFormService.get_league_table(league_id)
        return JsonResponse({'standings': table})