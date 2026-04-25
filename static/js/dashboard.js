let goalsByPlayerChart = null;
let goalsByTeamChart = null;
let teamComparisonChart = null;
let eventTypesChart = null;

async function loadFilters() {
    try {
        const leaguesResponse = await fetch('/api/leagues/');
        const leaguesData = await leaguesResponse.json();
        const leagueSelect = document.getElementById('leagueFilter');
        leaguesData.results.forEach(league => {
            const option = document.createElement('option');
            option.value = league.id;
            option.textContent = league.name;
            leagueSelect.appendChild(option);
        });

        const teamsResponse = await fetch('/api/teams/');
        const teamsData = await teamsResponse.json();
        const teamSelect = document.getElementById('teamFilter');
        teamsData.results.forEach(team => {
            const option = document.createElement('option');
            option.value = team.id;
            option.textContent = team.name;
            teamSelect.appendChild(option);
        });

        document.getElementById('compareTeam1').innerHTML = teamSelect.innerHTML;
        document.getElementById('compareTeam2').innerHTML = teamSelect.innerHTML;
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

async function loadDashboardData() {
    try {
        const response = await fetch('/api/analytics/dashboard/');
        const data = await response.json();

        document.getElementById('stat-leagues').textContent = data.summary.total_leagues;
        document.getElementById('stat-teams').textContent = data.summary.total_teams;
        document.getElementById('stat-players').textContent = data.summary.total_players;
        document.getElementById('stat-matches').textContent = data.summary.total_matches;

        renderGoalsByPlayerChart(data.top_scorers);
        renderGoalsByTeamChart(data.top_scorers);
        renderEventTypesChart(data.top_scorers);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function renderGoalsByPlayerChart(scorers) {
    const ctx = document.getElementById('goalsByPlayerChart').getContext('2d');

    if (goalsByPlayerChart) {
        goalsByPlayerChart.destroy();
    }

    goalsByPlayerChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: scorers.slice(0, 5).map(s => s.player.name),
            datasets: [{
                data: scorers.slice(0, 5).map(s => s.goals),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function renderGoalsByTeamChart(scorers) {
    const ctx = document.getElementById('goalsByTeamChart').getContext('2d');

    if (goalsByTeamChart) {
        goalsByTeamChart.destroy();
    }

    const teamGoals = {};
    scorers.forEach(s => {
        const teamName = s.player.team_name;
        teamGoals[teamName] = (teamGoals[teamName] || 0) + s.goals;
    });

    const sortedTeams = Object.entries(teamGoals)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

    goalsByTeamChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedTeams.map(t => t[0]),
            datasets: [{
                label: 'Goles',
                data: sortedTeams.map(t => t[1]),
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function compareTeams() {
    const team1Id = document.getElementById('compareTeam1').value;
    const team2Id = document.getElementById('compareTeam2').value;

    if (!team1Id || !team2Id) {
        alert('Seleccione ambos equipos');
        return;
    }

    try {
        const response = await fetch(`/reports/team-comparison/?team1=${team1Id}&team2=${team2Id}`);
        const data = await response.json();

        const ctx = document.getElementById('teamComparisonChart').getContext('2d');

        if (teamComparisonChart) {
            teamComparisonChart.destroy();
        }

        teamComparisonChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Partidos', 'Victorias', 'Empates', 'Goles F', 'Goles C'],
                datasets: [
                    {
                        label: data.team1.team,
                        data: [
                            data.team1.matches,
                            data.team1.wins,
                            data.team1.draws,
                            data.team1.goals_for,
                            data.team1.goals_against
                        ],
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 2
                    },
                    {
                        label: data.team2.team,
                        data: [
                            data.team2.matches,
                            data.team2.wins,
                            data.team2.draws,
                            data.team2.goals_for,
                            data.team2.goals_against
                        ],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error comparing teams:', error);
    }
}

function renderEventTypesChart(scorers) {
    const ctx = document.getElementById('eventTypesChart').getContext('2d');

    if (eventTypesChart) {
        eventTypesChart.destroy();
    }

    const eventCounts = {
        'Goles': 0,
        'Asistencias': 0,
        'Tiros': 0,
        'Faltas': 0
    };

    scorers.forEach(s => {
        eventCounts['Goles'] += s.goals;
        eventCounts['Asistencias'] += s.assists;
        eventCounts['Tiros'] += s.shots;
        eventCounts['Faltas'] += s.fouls;
    });

    eventTypesChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: Object.keys(eventCounts),
            datasets: [{
                data: Object.values(eventCounts),
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(255, 99, 132, 0.7)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function applyFilters() {
    const league = document.getElementById('leagueFilter').value;
    const team = document.getElementById('teamFilter').value;
    const season = document.getElementById('seasonFilter').value;

    console.log('Filters applied:', { league, team, season });
}

document.addEventListener('DOMContentLoaded', () => {
    loadFilters();
    loadDashboardData();
});