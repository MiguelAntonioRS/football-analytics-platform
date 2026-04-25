let radarChart = null;
let comparisonChart = null;

async function loadPlayers() {
    try {
        const response = await fetch('/api/players/');
        const data = await response.json();
        
        const select1 = document.getElementById('player1Select');
        const select2 = document.getElementById('player2Select');

        data.results.forEach(player => {
            const option1 = document.createElement('option');
            option1.value = player.id;
            option1.textContent = `${player.name} (${player.team_name})`;
            select1.appendChild(option1);

            const option2 = document.createElement('option');
            option2.value = player.id;
            option2.textContent = `${player.name} (${player.team_name})`;
            select2.appendChild(option2);
        });

        const urlParams = new URLSearchParams(window.location.search);
        const player1Id = urlParams.get('player1');
        if (player1Id) {
            select1.value = player1Id;
        }
    } catch (error) {
        console.error('Error loading players:', error);
    }
}

async function comparePlayers() {
    const player1Id = document.getElementById('player1Select').value;
    const player2Id = document.getElementById('player2Select').value;

    if (!player1Id || !player2Id) {
        alert('Seleccione ambos jugadores');
        return;
    }

    try {
        const response = await fetch(`/analytics/player-comparison/?player1=${player1Id}&player2=${player2Id}`);
        const data = await response.json();

        renderRadarChart(data.player1, data.player2);
        renderComparisonChart(data.player1, data.player2);
        renderComparisonAnalysis(data.player1, data.player2);
    } catch (error) {
        console.error('Error comparing players:', error);
    }
}

function renderRadarChart(p1, p2) {
    const ctx = document.getElementById('radarChart').getContext('2d');

    if (radarChart) {
        radarChart.destroy();
    }

    radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Goles', 'Asistencias', 'xG', 'Pases Clave', 'Entradas', 'Impact Score'],
            datasets: [
                {
                    label: p1.name,
                    data: [p1.goals, p1.assists, p1.xg.total_xg, p1.key_passes, p1.tackles, p1.impact_score],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2
                },
                {
                    label: p2.name,
                    data: [p2.goals, p2.assists, p2.xg.total_xg, p2.key_passes, p2.tackles, p2.impact_score],
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
}

function renderComparisonChart(p1, p2) {
    const ctx = document.getElementById('comparisonChart').getContext('2d');

    if (comparisonChart) {
        comparisonChart.destroy();
    }

    const maxValues = {
        goals: Math.max(p1.goals, p2.goals) || 1,
        assists: Math.max(p1.assists, p2.assists) || 1,
        xg: Math.max(p1.xg.total_xg, p2.xg.total_xg) || 1,
        key_passes: Math.max(p1.key_passes, p2.key_passes) || 1,
        tackles: Math.max(p1.tackles, p2.tackles) || 1
    };

    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Goles', 'Asistencias', 'xG', 'Pases Clave', 'Entradas'],
            datasets: [
                {
                    label: p1.name,
                    data: [
                        (p1.goals / maxValues.goals) * 100,
                        (p1.assists / maxValues.assists) * 100,
                        (p1.xg.total_xg / maxValues.xg) * 100,
                        (p1.key_passes / maxValues.key_passes) * 100,
                        (p1.tackles / maxValues.tackles) * 100
                    ],
                    backgroundColor: 'rgba(54, 162, 235, 0.7)'
                },
                {
                    label: p2.name,
                    data: [
                        (p2.goals / maxValues.goals) * 100,
                        (p2.assists / maxValues.assists) * 100,
                        (p2.xg.total_xg / maxValues.xg) * 100,
                        (p2.key_passes / maxValues.key_passes) * 100,
                        (p2.tackles / maxValues.tackles) * 100
                    ],
                    backgroundColor: 'rgba(255, 99, 132, 0.7)'
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Porcentaje (%)'
                    }
                }
            }
        }
    });
}

function renderComparisonAnalysis(p1, p2) {
    const container = document.getElementById('comparisonAnalysis');
    
    let html = '<div class="row">';
    
    const stats = [
        { name: 'Goles', p1: p1.goals, p2: p2.goals, higher: p1.goals > p2.goals },
        { name: 'Asistencias', p1: p1.assists, p2: p2.assists, higher: p1.assists > p2.assists },
        { name: 'xG Total', p1: p1.xg.total_xg.toFixed(2), p2: p2.xg.total_xg.toFixed(2), higher: p1.xg.total_xg > p2.xg.total_xg },
        { name: 'xG Difference', p1: p1.xg.xg_difference.toFixed(2), p2: p2.xg.xg_difference.toFixed(2), higher: p1.xg.xg_difference > p2.xg.xg_difference },
        { name: 'Pases Clave', p1: p1.key_passes, p2: p2.key_passes, higher: p1.key_passes > p2.key_passes },
        { name: 'Entradas', p1: p1.tackles, p2: p2.tackles, higher: p1.tackles > p2.tackles },
        { name: 'Impact Score', p1: p1.impact_score, p2: p2.impact_score, higher: p1.impact_score > p2.impact_score }
    ];

    stats.forEach(stat => {
        const winner = stat.higher ? p1.name : p2.name;
        const p1Val = stat.higher ? stat.p1 : stat.p2;
        const p2Val = stat.higher ? stat.p2 : stat.p1;
        
        html += `
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h6>${stat.name}</h6>
                        <div class="row">
                            <div class="col-5 text-end">
                                <strong>${p1.name}</strong><br>
                                <span class="${stat.higher ? 'text-success' : ''}">${stat.p1}</span>
                            </div>
                            <div class="col-2 text-center">
                                <span class="badge bg-secondary">VS</span>
                            </div>
                            <div class="col-5 text-start">
                                <strong>${p2.name}</strong><br>
                                <span class="${!stat.higher ? 'text-success' : ''}">${stat.p2}</span>
                            </div>
                        </div>
                        <div class="progress mt-2" style="height: 5px;">
                            <div class="progress-bar" style="width: ${(p1Val / (parseFloat(p1Val) + parseFloat(p2Val))) * 100}%"></div>
                        </div>
                        <small class="text-muted">Ganador: ${winner}</small>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    container.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', loadPlayers);