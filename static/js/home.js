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

        renderTopScorersChart(data.top_scorers);
        renderTopAssistsChart(data.top_assists);
        renderRecentMatches(data.recent_matches);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function renderTopScorersChart(scorers) {
    const ctx = document.getElementById('topScorersChart').getContext('2d');
    if (!ctx) return;

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
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: textColor, stepSize: 1 }
                },
                x: {
                    ticks: { color: textColor }
                }
            }
        }
    });
}

function renderTopAssistsChart(assists) {
    const ctx = document.getElementById('topAssistsChart').getContext('2d');
    if (!ctx) return;

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
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: textColor, stepSize: 1 }
                },
                x: {
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