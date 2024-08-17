// Used to render the Chart.js donut chart in dashboard-area-3
function renderCompletionChart(completedPaths, remainingPaths, completedModules, remainingModules, completedLessons, remainingLessons) {
    var ctx = document.getElementById('completionChart').getContext('2d');
    var completionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Completed Paths', 'Remaining Paths', 'Completed Modules', 'Remaining Modules', 'Completed Lessons', 'Remaining Lessons'],
            datasets: [{
                label: 'Completion Status',
                data: [
                    completedPaths,
                    remainingPaths,
                    completedModules,
                    remainingModules,
                    completedLessons,
                    remainingLessons
                ],
                backgroundColor: [
                    'rgba(34, 139, 34, 0.6)',    // Completed Paths - Dark Green
                    'rgba(255, 69, 58, 0.6)',    // Remaining Paths - Bright Red
                    'rgba(60, 179, 113, 0.6)',   // Completed Modules - Medium Green
                    'rgba(255, 135, 27, 0.6)',   // Remaining Modules - Dark Orange
                    'rgba(144, 238, 144, 0.6)',  // Completed Lessons - Light Green
                    'rgba(255, 165, 0, 0.6)'     // Remaining Lessons - Orange
                ],
                borderColor: [
                    'rgba(34, 139, 34, 1)',    // Completed Paths - Dark Green
                    'rgba(255, 69, 58, 1)',    // Remaining Paths - Bright Red
                    'rgba(60, 179, 113, 1)',   // Completed Modules - Medium Green
                    'rgba(255, 140, 0, 1)',    // Remaining Modules - Dark Orange
                    'rgba(144, 238, 144, 1)',  // Completed Lessons - Light Green
                    'rgba(255, 165, 0, 1)'     // Remaining Lessons - Orange
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
