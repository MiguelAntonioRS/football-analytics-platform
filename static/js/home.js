let topScorersChart = null;
let topAssistsChart = null;

async function loadDashboardData() {
    try {
        const response = await fetch('/api/analytics/dashboard/');
        const data = await response.json();

        document.getElementById('total-leagues').textContent = data.summary.total_leagues;
        document.getElementById('total-teams').textContent = data.summary.total_teams;
        document.getElementById('total-players').textContent = data.summary.total_players;
        document.getElementById('total-matches').textContent = data.summary.total_matches;
        document.getElementById('total-goals').textContent = data.summary.total_goals;
        document.getElementById('avg-goals').textContent = data.summary.avg_goals_per_match.toFixed(2);
        document.getElementById('matches-played').textContent = data.summary.total_matches;

        renderTopScorersChart(data.top_scorers);
        renderTopAssistsChart(data.top_assists);
        renderRecentMatches(data.recent_matches);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function renderTopScorersChart(scorers) {
    const ctx = document.getElementById('topScorersChart').getContext('2d');

    if (topScorersChart) {
        topScorersChart.destroy();
    }

    topScorersChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: scorers.map(s => s.player.name),
            datasets: [{
                label: 'Goles',
                data: scorers.map(s => s.goals),
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
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

function renderTopAssistsChart(assists) {
    const ctx = document.getElementById('topAssistsChart').getContext('2d');

    if (topAssistsChart) {
        topAssistsChart.destroy();
    }

    topAssistsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: assists.map(a => a.player.name),
            datasets: [{
                label: 'Asistencias',
                data: assists.map(a => a.assists),
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                borderColor: 'rgba(75, 192, 192, 1)',
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
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

function renderRecentMatches(matches) {
    const tbody = document.getElementById('recentMatchesBody');
    tbody.innerHTML = '';

    matches.forEach(match => {
        const row = document.createElement('tr');
        const date = new Date(match.date);
        row.innerHTML = `
            <td>${date.toLocaleDateString()}</td>
            <td>${match.home_team}</td>
            <td><strong>${match.home_score} - ${match.away_score}</strong></td>
            <td>${match.away_team}</td>
        `;
        tbody.appendChild(row);
    });
}

document.addEventListener('DOMContentLoaded', loadDashboardData);