import csv
import json

# Read the CSV file
with open('transactions_cleaned.csv', 'r') as f:
    reader = csv.DictReader(f)
    transactions = list(reader)

# Convert to JSON
transactions_json = json.dumps(transactions, indent=2)

# Read the dashboard template and embed data
dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transaction Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f7fa;
            color: #2c3e50;
            padding: 20px;
        }

        .container {
            max-width: 1800px;
            margin: 0 auto;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }

        .filter-panel {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .filter-panel h3 {
            margin-bottom: 20px;
            color: #667eea;
        }

        .filter-controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
        }

        .filter-group label {
            font-weight: 600;
            margin-bottom: 8px;
            color: #555;
            font-size: 0.9em;
        }

        .filter-group input,
        .filter-group select {
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 0.95em;
            transition: border-color 0.3s;
        }

        .filter-group input:focus,
        .filter-group select:focus {
            outline: none;
            border-color: #667eea;
        }

        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
        }

        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }

        .checkbox-group label {
            margin: 0;
            cursor: pointer;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-left: 4px solid #667eea;
            transition: transform 0.2s;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .stat-card h3 {
            color: #888;
            font-size: 0.9em;
            font-weight: 600;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stat-card .value {
            font-size: 2.2em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 5px;
        }

        .stat-card .subtitle {
            color: #999;
            font-size: 0.9em;
        }

        .stat-card.success { border-left-color: #2ecc71; }
        .stat-card.warning { border-left-color: #f39c12; }
        .stat-card.danger { border-left-color: #e74c3c; }
        .stat-card.info { border-left-color: #3498db; }

        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .chart-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .chart-card h3 {
            margin-bottom: 20px;
            color: #2c3e50;
            font-size: 1.2em;
        }

        .chart-container {
            position: relative;
            height: 300px;
        }

        .table-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            overflow-x: auto;
        }

        .table-card h3 {
            margin-bottom: 20px;
            color: #2c3e50;
            font-size: 1.2em;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #555;
            border-bottom: 2px solid #dee2e6;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #f0f0f0;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .customer-row {
            cursor: pointer;
            transition: background-color 0.2s;
        }

        .customer-row:hover {
            background: #e3f2fd !important;
        }

        .customer-row.selected {
            background: #2196f3 !important;
            color: white;
        }

        .customer-row.selected:hover {
            background: #1976d2 !important;
        }

        .highlighted-transaction {
            background-color: #fff9c4 !important;
            animation: highlight-fade 2s ease-in-out;
        }

        @keyframes highlight-fade {
            0% { background-color: #ffeb3b; }
            100% { background-color: #fff9c4; }
        }

        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }

        .status-created { background: #d4edda; color: #155724; }
        .status-cancelled { background: #f8d7da; color: #721c24; }
        .status-approved { background: #d1ecf1; color: #0c5460; }
        .status-captured { background: #d4edda; color: #155724; }

        .duplicate-info {
            margin-top: 10px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
            font-size: 0.9em;
            color: #666;
        }

        @media (max-width: 768px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Transaktionsanalyse Dashboard</h1>
            <p>Umfassende Analyse der Unternehmenstransaktionen</p>
        </div>

        <div class="filter-panel">
            <h3>🔍 Datenfilter</h3>
            <div class="filter-controls">
                <div class="filter-group">
                    <label>Statusfilter</label>
                    <select id="statusFilter">
                        <option value="all">Alle Status</option>
                        <option value="CREATED">Nur Erstellt</option>
                        <option value="CANCELLED">Nur Storniert</option>
                        <option value="APPROVED">Nur Genehmigt</option>
                        <option value="CAPTURED">Nur Erfasst</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Datum Von</label>
                    <input type="date" id="dateFrom">
                </div>
                <div class="filter-group">
                    <label>Datum Bis</label>
                    <input type="date" id="dateTo">
                </div>
                <div class="filter-group">
                    <label>Kundensuche</label>
                    <input type="text" id="customerSearch" placeholder="Nach Kundenname suchen...">
                </div>
            </div>
            <div class="checkbox-group">
                <input type="checkbox" id="excludeDuplicateNames">
                <label for="excludeDuplicateNames">Doppelte Namen ausschließen (erste Vorkommen behalten)</label>
            </div>
            <div class="checkbox-group">
                <input type="checkbox" id="excludeDuplicateNameAmount">
                <label for="excludeDuplicateNameAmount">Doppelte Name + Betrag ausschließen (erste Vorkommen behalten)</label>
            </div>
            <div id="duplicateInfo" class="duplicate-info" style="display: none;"></div>
        </div>

        <div id="statsGrid" class="stats-grid"></div>

        <div class="charts-grid">
            <div class="chart-card">
                <h3>Tägliches Transaktionsvolumen</h3>
                <div class="chart-container">
                    <canvas id="dailyVolumeChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h3>Transaktionsstatus Verteilung</h3>
                <div class="chart-container">
                    <canvas id="statusChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h3>Stündliches Aktivitätsmuster</h3>
                <div class="chart-container">
                    <canvas id="hourlyChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h3>Betragsverteilung</h3>
                <div class="chart-container">
                    <canvas id="amountChart"></canvas>
                </div>
            </div>
        </div>

        <div class="table-card">
            <h3>Top 15 Kunden nach Gesamtwert</h3>
            <table id="topCustomersTable"></table>
        </div>

        <div class="table-card">
            <h3>Alle Transaktionen</h3>
            <table id="recentTransactionsTable"></table>
        </div>
    </div>

    <script>
        // Embedded transaction data
        const TRANSACTIONS_DATA = ''' + transactions_json + ''';

        let allTransactions = TRANSACTIONS_DATA;
        let filteredData = [];
        let charts = {};
        let selectedCustomer = null; // Track selected customer for filtering

        function initializeFilters() {
            // Set date range based on data
            if (allTransactions.length > 0) {
                const dates = allTransactions.map(t => new Date(t.timestamp));
                const minDate = new Date(Math.min(...dates));
                const maxDate = new Date(Math.max(...dates));

                document.getElementById('dateFrom').value = minDate.toISOString().split('T')[0];
                document.getElementById('dateTo').value = maxDate.toISOString().split('T')[0];
            }

            // Add event listeners
            document.getElementById('statusFilter').addEventListener('change', applyFilters);
            document.getElementById('dateFrom').addEventListener('change', applyFilters);
            document.getElementById('dateTo').addEventListener('change', applyFilters);
            document.getElementById('customerSearch').addEventListener('input', applyFilters);
            document.getElementById('excludeDuplicateNames').addEventListener('change', applyFilters);
            document.getElementById('excludeDuplicateNameAmount').addEventListener('change', applyFilters);
        }

        function applyFilters() {
            let data = [...allTransactions];

            // Status filter
            const statusFilter = document.getElementById('statusFilter').value;
            if (statusFilter !== 'all') {
                data = data.filter(t => t.status === statusFilter);
            }

            // Date filters
            const dateFrom = new Date(document.getElementById('dateFrom').value);
            const dateTo = new Date(document.getElementById('dateTo').value);
            dateTo.setHours(23, 59, 59); // Include full day

            data = data.filter(t => {
                const tDate = new Date(t.timestamp);
                return tDate >= dateFrom && tDate <= dateTo;
            });

            // Customer search from input field (not from selection)
            const customerSearch = document.getElementById('customerSearch').value.toLowerCase();
            if (customerSearch && !selectedCustomer) {
                data = data.filter(t => t.customer_name.toLowerCase().includes(customerSearch));
            }

            const originalCount = data.length;
            const originalTotal = data.reduce((sum, t) => sum + parseFloat(t.amount), 0);

            // Duplicate filters
            const excludeDupNames = document.getElementById('excludeDuplicateNames').checked;
            const excludeDupNameAmount = document.getElementById('excludeDuplicateNameAmount').checked;

            if (excludeDupNames) {
                const seen = new Set();
                data = data.filter(t => {
                    if (seen.has(t.customer_name)) {
                        return false;
                    }
                    seen.add(t.customer_name);
                    return true;
                });
            }

            if (excludeDupNameAmount) {
                const seen = new Set();
                data = data.filter(t => {
                    const key = `${t.customer_name}|${t.amount}`;
                    if (seen.has(key)) {
                        return false;
                    }
                    seen.add(key);
                    return true;
                });
            }

            // Show duplicate info
            const duplicateInfo = document.getElementById('duplicateInfo');
            if (excludeDupNames || excludeDupNameAmount) {
                const removed = originalCount - data.length;
                const removedValue = originalTotal - data.reduce((sum, t) => sum + parseFloat(t.amount), 0);
                duplicateInfo.style.display = 'block';
                duplicateInfo.innerHTML = `
                    <strong>Duplikate entfernt:</strong> ${removed} Transaktionen
                    (€${removedValue.toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})})
                `;
            } else {
                duplicateInfo.style.display = 'none';
            }

            filteredData = data;
            updateDashboard();
        }

        function updateDashboard() {
            updateStats();
            updateCharts();
            updateTables();
        }

        function updateStats() {
            const total = filteredData.reduce((sum, t) => sum + parseFloat(t.amount), 0);
            const avg = total / filteredData.length || 0;

            const amounts = filteredData.map(t => parseFloat(t.amount)).sort((a, b) => a - b);
            const median = amounts.length ? amounts[Math.floor(amounts.length / 2)] : 0;

            const statusCounts = {};
            filteredData.forEach(t => {
                statusCounts[t.status] = (statusCounts[t.status] || 0) + 1;
            });

            const createdCount = statusCounts['CREATED'] || 0;
            const cancelledCount = statusCounts['CANCELLED'] || 0;
            const successRate = filteredData.length ? ((filteredData.length - cancelledCount) / filteredData.length * 100) : 0;

            const uniqueCustomers = new Set(filteredData.map(t => t.customer_name)).size;

            const dates = filteredData.map(t => new Date(t.timestamp));
            const daysDiff = dates.length ? Math.ceil((Math.max(...dates) - Math.min(...dates)) / (1000 * 60 * 60 * 24)) + 1 : 0;

            const statsHTML = `
                <div class="stat-card success">
                    <h3>Gesamttransaktionen</h3>
                    <div class="value">${filteredData.length}</div>
                    <div class="subtitle">${uniqueCustomers} eindeutige Kunden</div>
                </div>
                <div class="stat-card info">
                    <h3>Gesamtwert</h3>
                    <div class="value">€${total.toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                    <div class="subtitle">Über ${daysDiff} Tage</div>
                </div>
                <div class="stat-card">
                    <h3>Durchschnittliche Transaktion</h3>
                    <div class="value">€${avg.toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                    <div class="subtitle">Median: €${median.toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                </div>
                <div class="stat-card ${successRate >= 95 ? 'success' : 'warning'}">
                    <h3>Erfolgsquote</h3>
                    <div class="value">${successRate.toFixed(1)}%</div>
                    <div class="subtitle">${cancelledCount} storniert</div>
                </div>
                <div class="stat-card success">
                    <h3>Erstellt</h3>
                    <div class="value">${createdCount}</div>
                    <div class="subtitle">${((createdCount/filteredData.length)*100 || 0).toFixed(1)}% der Gesamtzahl</div>
                </div>
                <div class="stat-card info">
                    <h3>Größte Transaktion</h3>
                    <div class="value">€${Math.max(...amounts, 0).toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                    <div class="subtitle">Kleinste: €${Math.min(...amounts, 0).toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                </div>
            `;

            document.getElementById('statsGrid').innerHTML = statsHTML;
        }

        function updateCharts() {
            // Destroy existing charts
            Object.values(charts).forEach(chart => chart.destroy());
            charts = {};

            // Daily Volume Chart
            const dailyData = {};
            filteredData.forEach(t => {
                const date = new Date(t.timestamp).toISOString().split('T')[0];
                dailyData[date] = (dailyData[date] || 0) + parseFloat(t.amount);
            });

            const sortedDates = Object.keys(dailyData).sort();

            charts.daily = new Chart(document.getElementById('dailyVolumeChart'), {
                type: 'line',
                data: {
                    labels: sortedDates,
                    datasets: [{
                        label: 'Tägliches Volumen (EUR)',
                        data: sortedDates.map(date => dailyData[date]),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    }
                }
            });

            // Status Distribution
            const statusCounts = {};
            filteredData.forEach(t => {
                statusCounts[t.status] = (statusCounts[t.status] || 0) + 1;
            });

            charts.status = new Chart(document.getElementById('statusChart'), {
                type: 'doughnut',
                data: {
                    labels: Object.keys(statusCounts),
                    datasets: [{
                        data: Object.values(statusCounts),
                        backgroundColor: ['#2ecc71', '#e74c3c', '#3498db', '#f39c12']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

            // Hourly Pattern
            const hourlyData = new Array(24).fill(0);
            filteredData.forEach(t => {
                const hour = new Date(t.timestamp).getHours();
                hourlyData[hour]++;
            });

            charts.hourly = new Chart(document.getElementById('hourlyChart'), {
                type: 'bar',
                data: {
                    labels: Array.from({length: 24}, (_, i) => `${i}:00`),
                    datasets: [{
                        label: 'Transaktionen',
                        data: hourlyData,
                        backgroundColor: '#9b59b6'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    }
                }
            });

            // Amount Distribution
            const bins = [0, 1000, 2000, 3000, 4000, 5000, 10000];
            const binCounts = new Array(bins.length - 1).fill(0);
            filteredData.forEach(t => {
                const amount = parseFloat(t.amount);
                for (let i = 0; i < bins.length - 1; i++) {
                    if (amount >= bins[i] && amount < bins[i + 1]) {
                        binCounts[i]++;
                        break;
                    }
                }
            });

            charts.amount = new Chart(document.getElementById('amountChart'), {
                type: 'bar',
                data: {
                    labels: ['€0-1k', '€1k-2k', '€2k-3k', '€3k-4k', '€4k-5k', '€5k+'],
                    datasets: [{
                        label: 'Anzahl',
                        data: binCounts,
                        backgroundColor: '#3498db'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }

        function updateTables() {
            // Top Customers Table
            const customerTotals = {};
            filteredData.forEach(t => {
                const name = t.customer_name;
                if (!customerTotals[name]) {
                    customerTotals[name] = { total: 0, count: 0 };
                }
                customerTotals[name].total += parseFloat(t.amount);
                customerTotals[name].count++;
            });

            const topCustomers = Object.entries(customerTotals)
                .map(([name, data]) => ({
                    name,
                    total: data.total,
                    count: data.count,
                    avg: data.total / data.count
                }))
                .sort((a, b) => b.total - a.total)
                .slice(0, 15);

            const topCustomersHTML = `
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Kundenname</th>
                        <th>Gesamtwert</th>
                        <th>Transaktionen</th>
                        <th>Durchschn. Transaktion</th>
                    </tr>
                </thead>
                <tbody>
                    ${topCustomers.map((c, i) => `
                        <tr class="customer-row" data-customer-name="${c.name.replace(/"/g, '&quot;')}">
                            <td>${i + 1}</td>
                            <td>${c.name}</td>
                            <td>€${c.total.toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                            <td>${c.count}</td>
                            <td>€${c.avg.toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                        </tr>
                    `).join('')}
                </tbody>
            `;
            document.getElementById('topCustomersTable').innerHTML = topCustomersHTML;

            // Add click handlers to customer rows
            document.querySelectorAll('.customer-row').forEach(row => {
                row.addEventListener('click', function() {
                    const customerName = this.getAttribute('data-customer-name');
                    toggleCustomerFilter(customerName);
                });

                // Restore selection state
                if (selectedCustomer && row.getAttribute('data-customer-name') === selectedCustomer) {
                    row.classList.add('selected');
                }
            });

            // All Transactions Table - filter by selected customer if any
            let displayTransactions = [...filteredData];
            if (selectedCustomer) {
                displayTransactions = displayTransactions.filter(t => t.customer_name === selectedCustomer);
            }
            displayTransactions.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

            const allTransHTML = `
                <thead>
                    <tr>
                        <th>Datum & Zeit</th>
                        <th>Kunde</th>
                        <th>Betrag</th>
                        <th>Status</th>
                        <th>Referenz</th>
                    </tr>
                </thead>
                <tbody>
                    ${displayTransactions.map(t => `
                        <tr class="transaction-row" data-customer-name="${t.customer_name.replace(/"/g, '&quot;')}">
                            <td>${new Date(t.timestamp).toLocaleString('de-DE')}</td>
                            <td>${t.customer_name}</td>
                            <td>€${parseFloat(t.amount).toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                            <td><span class="status-badge status-${t.status.toLowerCase()}">${t.status}</span></td>
                            <td>${t.reference}</td>
                        </tr>
                    `).join('')}
                </tbody>
            `;
            document.getElementById('recentTransactionsTable').innerHTML = allTransHTML;
        }

        // Function to toggle customer filter
        function toggleCustomerFilter(customerName) {
            // If clicking the same customer, remove filter
            if (selectedCustomer === customerName) {
                selectedCustomer = null;
                document.getElementById('customerSearch').value = '';

                // Remove all selections
                document.querySelectorAll('.customer-row').forEach(row => {
                    row.classList.remove('selected');
                });

                // Update display
                updateTables();
            } else {
                // Select new customer
                selectedCustomer = customerName;
                document.getElementById('customerSearch').value = customerName;

                // Update selection state
                document.querySelectorAll('.customer-row').forEach(row => {
                    row.classList.remove('selected');
                    if (row.getAttribute('data-customer-name') === customerName) {
                        row.classList.add('selected');
                    }
                });

                // Update display and scroll
                updateTables();

                // Wait for DOM update, then scroll and highlight
                setTimeout(() => {
                    const transactionsTable = document.getElementById('recentTransactionsTable');
                    transactionsTable.scrollIntoView({ behavior: 'smooth', block: 'start' });

                    // Highlight all rows for this customer
                    document.querySelectorAll('.transaction-row').forEach(row => {
                        row.classList.remove('highlighted-transaction');
                        if (row.getAttribute('data-customer-name') === customerName) {
                            row.classList.add('highlighted-transaction');

                            // Remove highlight after animation
                            setTimeout(() => {
                                row.classList.remove('highlighted-transaction');
                            }, 3000);
                        }
                    });
                }, 100);
            }
        }

        // Initialize dashboard
        initializeFilters();
        applyFilters();
    </script>
</body>
</html>
'''

# Write the dashboard file
with open('dashboard.html', 'w') as f:
    f.write(dashboard_html)

print("Dashboard generated successfully!")
print("You can now open dashboard.html in your browser.")
