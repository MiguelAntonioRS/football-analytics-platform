async function loadStandings() {
    try {
        const response = await fetch('/api/analytics/standings/1/');
        const data = await response.json();
        renderStandings(data.standings);
        updateStats(data.standings);
    } catch (error) {
        console.error('Error loading standings:', error);
        document.getElementById('standingsBody').innerHTML = 
            '<tr><td colspan="10" class="text-center text-danger">Error al cargar</td></tr>';
    }
}

function renderStandings(standings) {
    const tbody = document.getElementById('standingsBody');
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

function updateStats(standings) {
    if (standings.length > 0) {
        document.getElementById('leader').textContent = standings[0].team;
        document.getElementById('matchesPlayed').textContent = standings[0].played + ' partidos';
    }
    
    document.getElementById('topScorer').textContent = 'Consultar API';
}

document.addEventListener('DOMContentLoaded', loadStandings);