
// State
let historyData = { dates: [], values: [] };
let currentForecast = { dates: [], values: [] };

document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
    
    // Theme Toggle
    document.getElementById('themeToggle').addEventListener('click', () => {
        const html = document.documentElement;
        const current = html.getAttribute('data-bs-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-bs-theme', next);
        const icon = document.querySelector('#themeToggle i');
        icon.className = next === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
        
        // Redraw chart to match theme
        if (historyData.dates.length > 0) renderChart();
    });
});

async function initDashboard() {
    showLoading(true);
    try {
        // Fetch History
        const histRes = await fetch('/api/history?hours=48'); // Last 2 days for context
        const histData = await histRes.json();
        
        if (histData.error) throw new Error(histData.error);
        
        historyData = histData;
        
        // Update Current Temp (Last historical point)
        if (historyData.values.length > 0) {
            const lastVal = historyData.values[historyData.values.length - 1];
            const lastDate = historyData.dates[historyData.dates.length - 1];
            document.getElementById('currentTemp').textContent = lastVal.toFixed(1);
            document.getElementById('latestTimestamp').textContent = new Date(lastDate).toLocaleString();
        }

        // Fetch Metrics
        const metricRes = await fetch('/api/metrics');
        const metricData = await metricRes.json();
        document.getElementById('rmseVal').textContent = metricData.rmse.toFixed(3);
        document.getElementById('maeVal').textContent = metricData.mae.toFixed(3);

        // Initial Forecast
        await updateForecast();
        
    } catch (err) {
        console.error("Init Error:", err);
        alert("Failed to load dashboard data.");
    } finally {
        showLoading(false);
    }
}

async function updateForecast() {
    showLoading(true);
    const model = document.getElementById('modelSelect').value;
    const horizon = document.getElementById('horizonSelect').value;
    
    // Endpoint mapping
    let endpoint = '/api/predict_24h';
    if (horizon === '7d') endpoint = '/api/predict_7d';
    
    try {
        const res = await fetch(`${endpoint}?model=${model}`);
        const data = await res.json();
        
        if (data.error) throw new Error(data.error);
        
        // Next Hour Metric
        if (data.forecast.length > 0) {
            document.getElementById('nextHourTemp').textContent = data.forecast[0].toFixed(1);
        }
        
        // Determine Forecast Trend
        const start = data.forecast[0];
        const end = data.forecast[data.forecast.length - 1];
        const diff = end - start;
        const trendEl = document.getElementById('trendText');
        const iconEl = document.getElementById('trendIcon');
        
        if (diff > 1.0) {
            trendEl.textContent = "Rising";
            iconEl.innerHTML = '<i class="fas fa-arrow-trend-up trend-up"></i>';
        } else if (diff < -1.0) {
            trendEl.textContent = "Falling";
            iconEl.innerHTML = '<i class="fas fa-arrow-trend-down trend-down"></i>';
        } else {
            trendEl.textContent = "Stable";
            iconEl.innerHTML = '<i class="fas fa-minus trend-stable"></i>';
        }

        // Generate Forecast Dates
        const lastHistDate = new Date(historyData.dates[historyData.dates.length - 1]);
        const forecastDates = data.hours.map(h => {
            const d = new Date(lastHistDate);
            d.setHours(d.getHours() + h);
            return d.toISOString();
        });
        
        currentForecast = {
            dates: forecastDates,
            values: data.forecast
        };
        
        renderChart();
        
    } catch (err) {
        console.error("Forecast Error:", err);
    } finally {
        showLoading(false);
    }
}

function renderChart() {
    const theme = document.documentElement.getAttribute('data-bs-theme');
    const isDark = theme === 'dark';
    
    const traceHist = {
        x: historyData.dates,
        y: historyData.values,
        mode: 'lines',
        name: 'Historical',
        line: { color: '#667eea', width: 3 }
    };
    
    const traceForecast = {
        x: currentForecast.dates,
        y: currentForecast.values,
        mode: 'lines',
        name: 'Forecast',
        line: { color: '#00c851', width: 3, dash: 'solid' } // Change dash if needed
    };
    
    // Connect the lines (Add last hist point to forecast)
    if (historyData.dates.length > 0) {
        traceForecast.x.unshift(historyData.dates[historyData.dates.length - 1]);
        traceForecast.y.unshift(historyData.values[historyData.values.length - 1]);
    }

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            color: isDark ? '#e0e0e0' : '#333333'
        },
        xaxis: {
            showgrid: true,
            gridcolor: isDark ? '#333' : '#eee',
            title: 'Time'
        },
        yaxis: {
            showgrid: true,
            gridcolor: isDark ? '#333' : '#eee',
            title: 'Temperature (°C)'
        },
        margin: { l: 50, r: 20, t: 30, b: 50 },
        legend: { orientation: 'h', y: 1.1 }
    };
    
    const config = { responsive: true, displayModeBar: false };
    
    Plotly.newPlot('weatherChart', [traceHist, traceForecast], layout, config);
}

function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) spinner.style.display = show ? 'block' : 'none';
}

function refreshForecast() {
    updateForecast();
}

function exportData() {
    alert("Export feature coming soon! (Download CSV/PDF)");
}
