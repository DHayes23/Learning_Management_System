// Used to render the Chart.js donut chart in dashboard-area-3
function renderCompletionChart(completedPaths, incompletePaths, completedModules, incompleteModules, completedLessons, incompleteLessons) {
    var ctx = document.getElementById('completionChart').getContext('2d');
    var completionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Completed Paths', 'Incomplete Paths', 'Completed Modules', 'Incomplete Modules', 'Completed Lessons', 'Incomplete Lessons'],
            datasets: [{
                label: 'Completion Status',
                data: [
                    completedPaths,
                    incompletePaths,
                    completedModules,
                    incompleteModules,
                    completedLessons,
                    incompleteLessons
                ],
                backgroundColor: [
                    'rgba(34, 139, 34, 0.6)',    // Completed Paths - Dark Green
                    'rgba(255, 69, 58, 0.6)',    // Incomplete Paths - Bright Red
                    'rgba(60, 179, 113, 0.6)',   // Completed Modules - Medium Green
                    'rgba(255, 135, 27, 0.6)',   // Incomplete Modules - Dark Orange
                    'rgba(144, 238, 144, 0.6)',  // Completed Lessons - Light Green
                    'rgba(255, 165, 0, 0.6)'     // Incomplete Lessons - Orange
                ],
                borderColor: [
                    'rgba(34, 139, 34, 1)',    // Completed Paths - Dark Green
                    'rgba(255, 69, 58, 1)',    // Incomplete Paths - Bright Red
                    'rgba(60, 179, 113, 1)',   // Completed Modules - Medium Green
                    'rgba(255, 140, 0, 1)',    // Incomplete Modules - Dark Orange
                    'rgba(144, 238, 144, 1)',  // Completed Lessons - Light Green
                    'rgba(255, 165, 0, 1)'     // Incomplete Lessons - Orange
                ],
                borderWidth: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#e2d0c5'
                    }
                },
            },
        }
    });
}

// Array of colors to be used for the leaderboard bars
const colors = [
    'rgba(255, 159, 64, 0.6)',  // Light Orange
    'rgba(54, 162, 235, 0.6)',  // Light Blue
    'rgba(153, 102, 255, 0.6)', // Light Purple
    'rgba(255, 206, 86, 0.6)',  // Light Yellow
    'rgba(123, 239, 178, 0.6)', // Light Green
    'rgba(75, 192, 192, 0.6)',  // Light Teal
    'rgba(255, 99, 132, 0.6)',  // Light Red
];

// Used to render the Chart.js horizontal bar chart in dashboard-area-4
function renderLeaderboardChart(labels, data) {
    // Create an array of background colors based on the number of students in the cohort
    const backgroundColors = labels.map((label, index) => {
        return colors[index % colors.length];
    });

    var ctx = document.getElementById('leaderboardChart').getContext('2d');
    var leaderboardChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Points',
                data: data,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color.replace('0.6', '1')),
                borderWidth: 3
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                y: {
                    ticks: {
                        display: false
                    }
                },
                
                x: {
                    beginAtZero: true
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'none',
                },
                datalabels: {
                    anchor: 'center',
                    align: 'center',
                    color: '#e2d0c5',
                    font: {
                        size: 18,
                        family: 'Arial',
                        weight: 'bold'
                    },
                    formatter: function(value, context) {
                        return context.chart.data.labels[context.dataIndex];  // Display the label inside the bar
                    }
                }
            },
        },
        plugins: [ChartDataLabels]
    });
}

// Used to initialise the 'Overall Progress' tooltip

document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
