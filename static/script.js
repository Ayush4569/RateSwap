document.getElementById('theme-switch').addEventListener('change', function() {
    const isDark = document.body.classList.toggle('dark-theme');
    document.body.classList.toggle('light-theme');
    updateChartTheme(isDark);
    
    // Update icon
    const icon = this.nextElementSibling.querySelector('i');
    icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    
    // Store theme preference
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    
    fetch('/toggle-theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
});

// Currency swap functionality
document.querySelector('.swap-icon').addEventListener('click', function() {
    const fromSelect = document.querySelector('select[name="from_currency"]');
    const toSelect = document.querySelector('select[name="to_currency"]');
    const temp = fromSelect.value;
    fromSelect.value = toSelect.value;
    toSelect.value = temp;
});

// Chart initialization
let rateChart = null;

function initChart() {
    const ctx = document.getElementById('rateChart').getContext('2d');
    rateChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Exchange Rate',
                data: [],
                borderColor: '#00bcd4',
                tension: 0.4,
                borderWidth: 2,
                pointRadius: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function updateChart(currency) {
    fetch(`/get-live-rates/${currency}`)
        .then(response => response.json())
        .then(data => {
            const times = data.data.map(point => point.time);
            const rates = data.data.map(point => point.rate);
            
            rateChart.data.labels = times;
            rateChart.data.datasets[0].data = rates;
            rateChart.data.datasets[0].label = `${currency}/INR Rate`;
            rateChart.update();
        });
}

function updateChartTheme(isDark) {
    if (rateChart) {
        rateChart.options.scales.y.grid.color = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
        rateChart.options.scales.y.ticks.color = isDark ? '#fff' : '#666';
        rateChart.options.scales.x.ticks.color = isDark ? '#fff' : '#666';
        rateChart.update();
    }
}

// Initialize chart and set up tab listeners
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    updateChart('USD');  // Initial load with USD/INR rate

    const storedTheme = localStorage.getItem('theme');
    if (storedTheme === 'dark') {
        document.getElementById('theme-switch').checked = true;
        document.body.classList.add('dark-theme');
        document.body.classList.remove('light-theme');
        updateChartTheme(true);
        const icon = document.querySelector('.switch i');
        icon.className = 'fas fa-sun';
    }

    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            // Update active state
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            e.target.classList.add('active');
            
            // Update chart
            updateChart(e.target.dataset.currency);
        });
    });
});
