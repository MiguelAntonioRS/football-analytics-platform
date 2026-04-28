let topScorersChart = null;
let topAssistsChart = null;

async function loadDashboardData() {
    try {
        // Load summary data
        const response = await fetch('/api/analytics/dashboard/');
        const data = await response.json();

        document.getElementById('total-leagues').textContent = data.summary.total_leagues;
        document.getElementById('total-teams').textContent = data.summary.total_teams;
        document.getElementById('total-players').textContent = data.summary.total_players;
        document.getElementById('total-matches').textContent = data.summary.total_matches;

        renderTopScorersChart(data.top_scorers);
        renderTopAssistsChart(data.top_assists);
        renderRecentMatches(data.recent_matches);
        
        // Load standings
        loadStandings();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

async function loadStandings() {
    try {
        const response = await fetch('/api/analytics/standings/1/');
        const data = await response.json();
        renderStandings(data.standings);
    } catch (error) {
        console.error('Error loading standings:', error);
        document.getElementById('standingsBody').innerHTML = 
            '<tr><td colspan="10" class="text-center text-danger">Error al cargar</td></tr>';
    }
}

function renderStandings(standings) {
    const tbody = document.getElementById('standingsBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    standings.forEach(team => {
        const row = document.createElement('tr');
        
        let posClass = '';
        if (team.position <= 4) posClass = 'table-success';
        else if (team.position <= 6) posClass = 'table-info';
        else if (team.position >= 18) posClass = 'table-danger';
        
        row.className = posClass;
        row.innerHTML = `
            <td><strong>${team.position}</strong></td>
            <td>${team.team}</td>
            <td>${team.played}</td>
            <td>${team.won}</td>
            <td>${team.drawn}</td>
            <td>${team.lost}</td>
            <td>${team.goals_for}</td>
            <td>${team.goals_against}</td>
            <td>${team.goal_difference > 0 ? '+' + team.goal_difference : team.goal_difference}</td>
            <td><strong>${team.points}</strong></td>
        `;
        tbody.appendChild(row);
    });
}

function renderTopScorersChart(scorers) {
    const ctx = document.getElementById('topScorersChart');
    if (!ctx) return;
    ctx = ctx.getContext('2d');

    if (topScorersChart) topScorersChart.destroy();

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#e0e0e0' : '#333';

    topScorersChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: scorers.slice(0, 5).map(s => s.player.name),
            datasets: [{
                label: 'Goles',
                data: scorers.slice(0, 5).map(s => s.goals),
                backgroundColor: 'rgba(40, 167, 69, 0.7)',
                borderColor: 'rgba(40, 167, 69, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { color: textColor, stepSize: 1 }
                },
                y: {
                    ticks: { color: textColor }
                }
            }
        }
    });
}

function renderTopAssistsChart(assists) {
    const ctx = document.getElementById('topAssistsChart');
    if (!ctx) return;
    ctx = ctx.getContext('2d');

    if (topAssistsChart) topAssistsChart.destroy();

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#e0e0e0' : '#333';

    topAssistsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: assists.slice(0, 5).map(a => a.player.name),
            datasets: [{
                label: 'Asistencias',
                data: assists.slice(0, 5).map(a => a.assists),
                backgroundColor: 'rgba(23, 162, 184, 0.7)',
                borderColor: 'rgba(23, 162, 184, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { color: textColor, stepSize: 1 }
                },
                y: {
                    ticks: { color: textColor }
                }
            }
        }
    });
}

function renderRecentMatches(matches) {
    const tbody = document.getElementById('recentMatchesBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    matches.forEach(match => {
        const date = new Date(match.date);
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${date.toLocaleDateString()}</td>
            <td><strong>${match.home_team}</strong></td>
            <td><span class="badge bg-success">${match.home_score} - ${match.away_score}</span></td>
            <td><strong>${match.away_team}</strong></td>
        `;
        tbody.appendChild(row);
    });
}

document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('regUsername').value,
        email: document.getElementById('regEmail').value,
        password: document.getElementById('regPassword').value,
        password_confirm: document.getElementById('regPasswordConfirm').value
    };

    try {
        const response = await fetch('/api/users/auth/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok) {
            alert('Registro exitoso! Ahora puedes iniciar sesión.');
            bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
        } else {
            alert('Error: ' + JSON.stringify(result));
        }
    } catch (error) {
        alert('Error de conexión');
    }
});

document.addEventListener('DOMContentLoaded', loadDashboardData);