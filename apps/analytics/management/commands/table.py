from apps.teams.models import Team
from apps.matches.models import Match

print('=== TABLA DE CLASIFICACION Premier League ===\n')

teams = Team.objects.all()[:20]
standings = []

for team in teams:
    matches = Match.objects.filter(status='finished').filter(
        home_team=team
    ) | Match.objects.filter(status='finished').filter(away_team=team)
    
    wins = draws = losses = gf = gc = 0
    for m in matches:
        if m.home_team == team:
            gf += m.home_score
            gc += m.away_score
            if m.home_score > m.away_score: wins += 1
            elif m.home_score == m.away_score: draws += 1
            else: losses += 1
        else:
            gf += m.away_score
            gc += m.home_score
            if m.away_score > m.home_score: wins += 1
            elif m.away_score == m.home_score: draws += 1
            else: losses += 1
    
    points = wins * 3 + draws
    standings.append({
        'team': team.name,
        'points': points,
        'played': wins + draws + losses,
        'won': wins,
        'drawn': draws,
        'lost': losses,
        'gf': gf,
        'gc': gc,
        'gd': gf - gc
    })

standings.sort(key=lambda x: (-x['points'], -x['gd'], -x['gf']))

print('Pos Equipo                  PJ  G   E   P   GF  GC  DG  Pts')
print('-' * 65)
for i, s in enumerate(standings[:20], 1):
    print(f'{i:>2}. {s["team"][:22]:<22} {s["played"]:>2}  {s["won"]:>2}  {s["drawn"]:>2}  {s["lost"]:>2}  {s["gf"]:>2}  {s["gc"]:>2} {s["gd"]:>3} {s["points"]:>3}')