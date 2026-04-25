async function loadLeaderboard() {
    try {
        const response = await fetch('/api/fantasy/leaderboard/weekly/');
        const data = await response.json();
        renderLeaderboard(data);
    } catch (error) {
        console.error('Error loading leaderboard:', error);
    }
}

function renderLeaderboard(entries) {
    const tbody = document.getElementById('leaderboardBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    entries.forEach((entry, i) => {
        const row = document.createElement('tr');
        const medal = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `${i + 1}`;
        row.innerHTML = `
            <td><strong>${medal}</strong></td>
            <td>${entry.username}</td>
            <td><strong>${entry.points}</strong></td>
        `;
        tbody.appendChild(row);
    });
}

async function loadAchievements() {
    try {
        const response = await fetch('/api/fantasy/achievements/my_achievements/');
        const data = await response.json();
        renderAchievements(data);
    } catch (error) {
        console.error('Error loading achievements:', error);
    }
}

function renderAchievements(achievements) {
    const container = document.getElementById('achievementsList');
    if (!container) return;
    container.innerHTML = '';

    achievements.forEach(ach => {
        const col = document.createElement('div');
        col.className = 'col-md-4 mb-3';
        col.innerHTML = `
            <div class="card ${ach.is_earned ? 'border-success' : ''}">
                <div class="card-body text-center">
                    <h1>${ach.icon}</h1>
                    <h5>${ach.name}</h5>
                    <p class="text-muted small">${ach.description}</p>
                    ${ach.is_earned 
                        ? '<span class="badge bg-success">✓ Desbloqueado</span>' 
                        : `<span class="badge bg-secondary">${ach.requirement} puntos requeridos</span>`}
                </div>
            </div>
        `;
        container.appendChild(col);
    });
}

async function loadPredictions() {
    try {
        const response = await fetch('/api/fantasy/predictions/available_matches/');
        const data = await response.json();
        renderPredictions(data);
    } catch (error) {
        console.error('Error loading matches:', error);
    }
}

function renderPredictions(matches) {
    const container = document.getElementById('availableMatches');
    if (!container) return;
    container.innerHTML = '';

    if (matches.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay partidos disponibles</p>';
        return;
    }

    matches.forEach(match => {
        const item = document.createElement('div');
        item.className = 'list-group-item';
        item.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h5>${match.match}</h5>
                    <small class="text-muted">${new Date(match.date).toLocaleString()}</small>
                </div>
                <button class="btn btn-sm btn-success" onclick="showPredictionForm(${match.id})">
                    Pronosticar
                </button>
            </div>
        `;
        container.appendChild(item);
    });
}

function showPredictionForm(matchId) {
    const homeScore = prompt('Goles equipo local:');
    const awayScore = prompt('Goles equipo visitante:');
    if (homeScore !== null && awayScore !== null) {
        submitPrediction(matchId, parseInt(homeScore), parseInt(awayScore));
    }
}

async function submitPrediction(matchId, homeScore, awayScore) {
    try {
        const response = await fetch('/api/fantasy/predictions/submit_prediction/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            },
            body: JSON.stringify({
                match_id: matchId,
                home_score: homeScore,
                away_score: awayScore
            })
        });
        if (response.ok) {
            alert('Pronóstico guardado!');
            loadPredictions();
        }
    } catch (error) {
        console.error('Error submitting prediction:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadLeaderboard();
    loadAchievements();
    loadPredictions();
});