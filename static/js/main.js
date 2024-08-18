// Used to render the Chart.js donut chart in dashboard-area-3
function renderCompletionChart(completedPaths, incompletePaths, completedModules, incompleteModules, completedLessons, incompleteLessons) {
    var ctx = document.getElementById('completionChart').getContext('2d');
    var originalData = [
        completedPaths,
        incompletePaths,
        completedModules,
        incompleteModules,
        completedLessons,
        incompleteLessons
    ];

    // Track the active segment
    var activeIndex = null;

    var completionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Completed Paths', 'Incomplete Paths', 'Completed Modules', 'Incomplete Modules', 'Completed Lessons', 'Incomplete Lessons'],
            datasets: [{
                label: 'Completion Status',
                data: [...originalData],
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
                        color: '#e2d0c5',
                        usePointStyle: false,
                        generateLabels: function(chart) {
                            return chart.data.labels.map(function(label, i) {
                                return {
                                    text: chart.data.datasets[0].data[i] !== 0 ? label : '\u0336' + label.split('').join('\u0336'),  // Add strikethrough if hidden
                                    fillStyle: chart.data.datasets[0].backgroundColor[i],
                                    hidden: chart.data.datasets[0].data[i] === 0, // Adjust the hidden property based on data visibility
                                    index: i,
                                    fontColor: '#e2d0c5',
                                };
                            });
                        }
                    },
                    onClick: function(e, legendItem) {
                        const index = legendItem.index;
                        const chart = this.chart;
                        const chartData = chart.data.datasets[0].data;

                        // Toggle visibility
                        if (chartData[index] === 0) {
                            chartData[index] = originalData[index]; // Restore the data
                        } else {
                            chartData[index] = 0; // Hide the data
                        }

                        // Update chart and legend
                        chart.update();
                    }
                },
                tooltip: {
                    enabled: false  // Disable tooltips to prevent clipping
                },
                datalabels: {
                    color: '#e2d0c5',
                    font: {
                        weight: 'bold',
                        family: 'Arial',
                        size: 18,
                    },
                    display: function(context) {
                        // Only display the label if the current segment is acctive
                        return context.dataIndex === activeIndex;
                    },
                    formatter: function(value) {
                        return value;  // Display the value (number of paths, modules or lessons) inside the segment
                    },
                }
            },
            onHover: function(event, chartElement) {
                if (chartElement.length) {
                    activeIndex = chartElement[0].index;
                } else {
                    activeIndex = null;
                }
                completionChart.update();
                event.native.target.style.cursor = chartElement[0] ? 'pointer' : 'default';
            },
            onClick: function(evt, activeElements) {
                const activeElement = activeElements[0];
                if (activeElement) {
                    const datasetIndex = activeElement.datasetIndex;
                    const index = activeElement.index;
                    const chartData = this.data.datasets[datasetIndex].data;

                    // Toggle visibility: hide if visible, restore original if hidden
                    if (chartData[index] !== 0) {
                        chartData[index] = 0;
                    } else {
                        chartData[index] = originalData[index];
                    }

                    // Redraw the chart
                    this.update();
                }
            }
        },
        plugins: [ChartDataLabels]
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
