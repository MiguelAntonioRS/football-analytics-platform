async function loadMatches() {
    try {
        const response = await fetch('/api/matches/?status=finished');
        const data = await response.json();
        const select = document.getElementById('matchSelect');
        data.results.forEach(match => {
            const option = document.createElement('option');
            option.value = match.id;
            option.textContent = `${match.home_team_name} ${match.home_score}-${match.away_score} ${match.away_team_name}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading matches:', error);
    }
}

async function loadShotMap() {
    const matchId = document.getElementById('matchSelect').value;
    if (!matchId) {
        alert('Seleccione un partido');
        return;
    }

    try {
        const response = await fetch(`/api/events/shots/?match=${matchId}`);
        const data = await response.json();
        renderShotMap(data.results);
    } catch (error) {
        console.error('Error loading shot map:', error);
    }
}

function renderShotMap(shots) {
    const goal_x = 105;
    const goal_y = 34;

    const shotsData = shots.map(shot => ({
        x: parseFloat(shot.x_coordinate),
        y: parseFloat(shot.y_coordinate),
        is_goal: shot.is_goal,
        xg: parseFloat(shot.xg_value),
        player: shot.player_name,
        minute: shot.minute
    }));

    const nonGoals = shotsData.filter(s => !s.is_goal);
    const goals = shotsData.filter(s => s.is_goal);

    const trace1 = {
        x: nonGoals.map(s => s.x),
        y: nonGoals.map(s => s.y),
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: nonGoals.map(s => Math.max(8, s.xg * 80)),
            color: nonGoals.map(s => s.xg),
            colorscale: 'Blues',
            symbol: 'x'
        },
        text: nonGoals.map(s => `${s.player} (${s.minute}')\nxG: ${s.xg.toFixed(3)}`),
        hoverinfo: 'text',
        name: 'Tiros'
    };

    const trace2 = {
        x: goals.map(s => s.x),
        y: goals.map(s => s.y),
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: goals.map(s => Math.max(12, s.xg * 80)),
            color: 'green',
            symbol: 'circle-open'
        },
        text: goals.map(s => `${s.player} (${s.minute}')\nxG: ${s.xg.toFixed(3)}`),
        hoverinfo: 'text',
        name: 'Goles'
    };

    const layout = {
        title: 'Mapa de Tiros',
        xaxis: {
            title: '',
            range: [0, 110],
            showgrid: false,
            zeroline: false
        },
        yaxis: {
            title: '',
            range: [0, 70],
            showgrid: false,
            zeroline: false
        },
        shapes: [
            {
                type: 'rect',
                x0: 0, y0: 0,
                x1: 110, y1: 70,
                line: {color: 'white', width: 2}
            },
            {
                type: 'rect',
                x0: 88, y0: 30,
                x1: 105, y1: 38,
                line: {color: 'white', width: 2, dash: 'dot'}
            }
        ],
        showlegend: true,
        plot_bgcolor: '#1a472a'
    };

    Plotly.newPlot('shotMap', [trace1, trace2], layout);
}

async function loadTopXgPlayers() {
    try {
        const response = await fetch('/api/analytics/top-xg/');
        const data = await response.json();

        const ctx = document.getElementById('topXgPlayersChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.slice(0, 10).map(p => p.player),
                datasets: [{
                    label: 'xG Total',
                    data: data.slice(0, 10).map(p => p.total_xg),
                    backgroundColor: 'rgba(54, 162, 235, 0.7)'
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: { legend: { display: false } }
            }
        });
    } catch (error) {
        console.error('Error loading top xG players:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadMatches();
    loadTopXgPlayers();
});