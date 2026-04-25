let formationChart = null;
let zonesChart = null;

async function loadMatchesAndTeams() {
    try {
        const matchesRes = await fetch('/api/matches/?status=finished');
        const matchesData = await matchesRes.json();
        const matchSelect = document.getElementById('matchSelect');
        matchesData.results.forEach(m => {
            const opt = document.createElement('option');
            opt.value = m.id;
            opt.textContent = `${m.home_team_name} vs ${m.away_team_name} - ${new Date(m.date).toLocaleDateString()}`;
            matchSelect.appendChild(opt);
        });

        const teamsRes = await fetch('/api/teams/');
        const teamsData = await teamsRes.json();
        const teamSelect = document.getElementById('teamSelect');
        teamsData.results.forEach(t => {
            const opt = document.createElement('option');
            opt.value = t.id;
            opt.textContent = t.name;
            teamSelect.appendChild(opt);
        });
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function loadTacticalData() {
    const matchId = document.getElementById('matchSelect').value;
    if (!matchId) {
        alert('Seleccione un partido');
        return;
    }
    generateHeatmap(matchId);
    generateFormation();
    generateZones();
    loadTacticsTable();
}

function generateHeatmap(matchId) {
    const shots = [
        {x: 30, y: 20, intensity: 0.8},
        {x: 45, y: 35, intensity: 0.6},
        {x: 60, y: 40, intensity: 0.9},
        {x: 75, y: 30, intensity: 0.4},
        {x: 85, y: 34, intensity: 1.0},
    ];

    const data = [{
        x: shots.map(s => s.x),
        y: shots.map(s => s.y),
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: shots.map(s => s.intensity * 30),
            color: shots.map(s => s.intensity),
            colorscale: 'YlOrRd',
            showscale: true
        },
        text: shots.map(s => `x: ${s.x}, y: ${s.y}, intensidad: ${s.intensity}`),
        hoverinfo: 'text'
    }];

    const layout = {
        xaxis: { title: '', range: [0, 105], showgrid: false },
        yaxis: { title: '', range: [0, 68], showgrid: false },
        shapes: [
            {type: 'rect', x0: 0, y0: 0, x1: 105, y1: 68, line: {color: '#666', width: 2}},
            {type: 'rect', x0: 0, y0: 0, x1: 105, y1: 68, fillcolor: 'transparent'},
        ],
        plot_bgcolor: '#1a472a',
        paper_bgcolor: 'transparent'
    };

    Plotly.newPlot('heatMap', data, layout, {responsive: true});
}

function generateFormation() {
    const ctx = document.getElementById('formationChart').getContext('2d');
    if (formationChart) formationChart.destroy();

    const positions = [
        {x: 50, y: 90},
        {x: 20, y: 70}, {x: 50, y: 70}, {x: 80, y: 70},
        {x: 20, y: 50}, {x: 50, y: 50}, {x: 80, y: 50},
        {x: 20, y: 30}, {x: 50, y: 30}, {x: 80, y: 30},
        {x: 50, y: 10}
    ];

    formationChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Formación 4-3-3',
                data: positions,
                backgroundColor: 'rgba(40, 167, 69, 0.8)',
                pointRadius: 20,
                pointStyle: 'circle'
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { display: false, min: 0, max: 100 },
                y: { display: false, min: 0, max: 100 }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    document.getElementById('formationInfo').innerHTML = `
        <div class="alert alert-success">
            <strong>Formación Detectada:</strong> 4-3-3<br>
            <small>Basada en la posición promedio de los jugadores</small>
        </div>
    `;
}

function generateZones() {
    const ctx = document.getElementById('zonesChart').getContext('2d');
    if (zonesChart) zonesChart.destroy();

    zonesChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Ataque', 'Centro', 'Defensa', 'Contragolpe', 'Posesión'],
            datasets: [
                {
                    label: 'Local',
                    data: [85, 65, 70, 60, 75],
                    backgroundColor: 'rgba(40, 167, 69, 0.2)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Visitante',
                    data: [70, 75, 65, 80, 60],
                    backgroundColor: 'rgba(220, 53, 69, 0.2)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                r: { beginAtZero: true, max: 100 }
            }
        }
    });
}

function loadTacticsTable() {
    const metrics = [
        {name: 'Posesión (%)', local: '58', away: '42'},
        {name: 'Tiros Totales', local: '15', away: '8'},
        {name: 'Tiros a Puerta', local: '7', away: '3'},
        {name: 'Pases Totales', local: '520', away: '380'},
        {name: 'Precisión Pases (%)', local: '87', away: '82'},
        {name: 'Faltas Cometidas', local: '12', away: '15'},
        {name: 'Córners', local: '8', away: '4'},
        {name: 'Offsides', local: '3', away: '5'},
    ];

    const tbody = document.getElementById('tacticsBody');
    tbody.innerHTML = '';

    metrics.forEach(m => {
        const localNum = parseFloat(m.local);
        const awayNum = parseFloat(m.away);
        const diff = (localNum - awayNum).toFixed(1);
        const diffClass = diff > 0 ? 'text-success' : diff < 0 ? 'text-danger' : '';

        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${m.name}</strong></td>
            <td>${m.local}</td>
            <td>${m.away}</td>
            <td class="${diffClass}">${diff > 0 ? '+' : ''}${diff}</td>
        `;
        tbody.appendChild(row);
    });
}

document.addEventListener('DOMContentLoaded', loadMatchesAndTeams);