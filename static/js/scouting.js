async function searchPlayers() {
    const params = new URLSearchParams();
    
    const minAge = document.getElementById('minAge').value;
    const maxAge = document.getElementById('maxAge').value;
    const minGoals = document.getElementById('minGoals').value;
    const minAssists = document.getElementById('minAssists').value;
    const minXg = document.getElementById('minXg').value;
    const position = document.getElementById('position').value;

    if (minAge) params.append('min_age', minAge);
    if (maxAge) params.append('max_age', maxAge);
    if (minGoals) params.append('min_goals', minGoals);
    if (minAssists) params.append('min_assists', minAssists);
    if (minXg) params.append('min_xg', minXg);
    if (position) params.append('position', position);

    try {
        const response = await fetch(`/analytics/scouting/?${params.toString()}`);
        const data = await response.json();
        renderScoutingResults(data.players);
    } catch (error) {
        console.error('Error searching players:', error);
    }
}

function renderScoutingResults(players) {
    const tbody = document.getElementById('scoutingBody');
    tbody.innerHTML = '';

    players.forEach(p => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${p.player}</strong></td>
            <td>${p.team}</td>
            <td>${p.age || 'N/A'}</td>
            <td><span class="badge bg-secondary">${translatePosition(p.position)}</span></td>
            <td><span class="text-success">${p.goals}</span></td>
            <td><span class="text-info">${p.assists}</span></td>
            <td><span class="text-warning">${p.xg.toFixed(2)}</span></td>
            <td><strong>${p.impact_score}</strong></td>
            <td>
                <button class="btn btn-sm btn-outline-success" onclick="compareWith('${p.player_id}')">
                    Comparar
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function translatePosition(position) {
    const positions = {
        'forward': 'DEL',
        'midfielder': 'MED',
        'defender': 'DEF',
        'goalkeeper': 'POR'
    };
    return positions[position] || position;
}

function compareWith(playerId) {
    window.location.href = `/compare/?player1=${playerId}`;
}

document.addEventListener('DOMContentLoaded', () => {
    searchPlayers();
});