function loadTrendsData() {
    renderGoalsTrend();
    renderFormChart();
    renderXgTrend();
}

function renderGoalsTrend() {
    const data = [{
        x: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        y: [3, 2, 4, 3, 5, 2, 4, 3, 5, 4],
        mode: 'lines+markers',
        name: 'Goles',
        line: {color: '#28a745', width: 3},
        marker: {size: 8}
    }];

    const layout = {
        xaxis: {title: 'Jornada'},
        yaxis: {title: 'Goles Totales', dtick: 1},
        plot_bgcolor: 'transparent',
        paper_bgcolor: 'transparent'
    };

    Plotly.newPlot('goalsTrendChart', data, layout, {responsive: true});
}

function renderFormChart() {
    const ctx = document.getElementById('formChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['G1', 'G2', 'G3', 'G4', 'G5'],
            datasets: [{
                label: 'Resultado',
                data: [3, 1, 3, 0, 3],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.7)',
                    'rgba(255, 193, 7, 0.7)',
                    'rgba(40, 167, 69, 0.7)',
                    'rgba(220, 53, 69, 0.7)',
                    'rgba(40, 167, 69, 0.7)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    display: false,
                    min: 0,
                    max: 4
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderXgTrend() {
    const ctx = document.getElementById('xgTrendChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['J1', 'J2', 'J3', 'J4', 'J5'],
            datasets: [
                {
                    label: 'xG',
                    data: [1.8, 2.1, 1.5, 2.3, 1.9],
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Goles',
                    data: [2, 2, 2, 3, 2],
                    borderColor: '#17a2b8',
                    backgroundColor: 'rgba(23, 162, 184, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', loadTrendsData);