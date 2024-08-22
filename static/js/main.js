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

// Used to render the Chart.js horizontal bar chart in dashboard-area-4
function renderLeaderboardChart(labels, data) {
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


// Used to handle the GSAP animations of the Path display
function toggleModules(pathId) {
    var modulesContainer = document.getElementById('modules-' + pathId);
    var selectedCard = document.getElementById('card-' + pathId);
    var titleElement = document.getElementById('title-' + pathId);
    var viewModulesButton = document.getElementById('button-' + pathId);
    var allCards = document.querySelectorAll('.path-card');
    var gridContainer = document.querySelector('.path-card-grid');
    var heading = document.getElementById('assigned-paths-heading');
    var body = document.body;
    var contentArea = document.querySelector('.content-area');
    var isSelected = modulesContainer.classList.contains('show');

    viewModulesButton.style.pointerEvents = 'none';
    viewModulesButton.style.opacity = '0.6';

    if (isSelected) {
        var tlClose = gsap.timeline({
            onComplete: function () {
                gsap.to(selectedCard, {
                    duration: 1.5,
                    width: selectedCard.dataset.originalWidth,
                    height: selectedCard.dataset.originalHeight,
                    padding: "1.5rem 1.5rem 2rem 1.5rem",
                    left: selectedCard.dataset.originalLeft,
                    top: selectedCard.dataset.originalTop,
                    onComplete: function () {
                        gsap.set(selectedCard, { position: '', clearProps: 'all' });
                        gridContainer.style.width = '';
                        gridContainer.style.height = '';
                        gridContainer.style.gridTemplateColumns = '';
                        gsap.to(allCards, { duration: 0.5, opacity: 1, transform: "translate(0, 0)", clearProps: 'all' });
                        gsap.to(heading, { duration: 0.5, y: "0px", opacity: 1 });
                        viewModulesButton.style.pointerEvents = 'auto';
                        viewModulesButton.style.opacity = '';
                    }
                });
            }
        });

        tlClose.to(modulesContainer.querySelectorAll('li'), {
            duration: 0.5,
            opacity: 0,
            y: "-20px",
            stagger: { each: 0.1, from: "end" },
            onComplete: function () {
                modulesContainer.style.display = 'none';
                modulesContainer.classList.remove('show');
            }
        }).to(titleElement, {
            duration: 0.5,
            fontSize: "1.5rem",
            ease: "power1.out",
        }, "-=0.3");

        tlClose.to(viewModulesButton, {
            duration: 0.5,
            width: "auto", 
            onComplete: function () {
                viewModulesButton.innerHTML = 'View Modules';
            }
        });

        body.style.overflow = ''; 
    } else {
        gsap.to(heading, { duration: 0.5, y: "-100px", opacity: 0 });

        window.scrollTo({ top: 0, behavior: 'smooth' });

        setTimeout(function () {
            body.style.overflow = 'hidden';

            gridContainer.style.width = gridContainer.offsetWidth + 'px';
            gridContainer.style.height = gridContainer.offsetHeight + 'px';
            gridContainer.style.gridTemplateColumns = getComputedStyle(gridContainer).gridTemplateColumns;

            allCards.forEach(function (card) {
                if (card !== selectedCard) {
                    gsap.to(card, { duration: 1, transform: "translateY(200%)", opacity: 0 });
                }
            });

            var cardRect = selectedCard.getBoundingClientRect();
            var contentRect = contentArea.getBoundingClientRect();

            selectedCard.dataset.originalLeft = cardRect.left + 'px';
            selectedCard.dataset.originalTop = cardRect.top + 'px';
            selectedCard.dataset.originalWidth = cardRect.width + 'px';
            selectedCard.dataset.originalHeight = cardRect.height + 'px';

            var contentCenterX = contentRect.left + contentRect.width / 2;
            var contentCenterY = contentRect.top + contentRect.height / 2;

            var newWidth = cardRect.width * 2;
            var newHeight = window.innerHeight * 0.9;
            var newLeft = contentCenterX - newWidth / 2;
            var newTop = contentCenterY - newHeight / 2 - 50;

            selectedCard.dataset.centerLeft = newLeft + 'px';
            selectedCard.dataset.centerTop = newTop + 'px';
            selectedCard.dataset.newWidth = newWidth + 'px';
            selectedCard.dataset.newHeight = newHeight + 'px';

            gsap.set(selectedCard, { position: 'fixed', left: cardRect.left, top: cardRect.top, width: cardRect.width, height: cardRect.height });

            gsap.to(viewModulesButton, {
                duration: 0.5,
                width: "auto", 
                onComplete: function () {
                    viewModulesButton.innerHTML = '<i class="back-icon fa-sharp fa-arrow-left"></i>Back';
                }
            });

            var tlOpen = gsap.timeline();

            tlOpen.to(selectedCard, {
                duration: 1,
                width: newWidth,
                height: newHeight,
                left: newLeft,
                top: newTop,
                padding: "2rem",
            });

            tlOpen.to(modulesContainer, {
                display: 'block',
                onStart: function() {
                    gsap.fromTo(modulesContainer.querySelectorAll('li'), 
                        { opacity: 0, y: "-50px" },  
                        { duration: 1.5, opacity: 1, y: "0px", stagger: { each: 0.25, from: "start" }, ease: "power1.out" }
                    );
                    modulesContainer.classList.add('show');
                }
            }, "-=0.5");

            tlOpen.to(titleElement, {
                duration: 0.5,
                fontSize: "2.5rem",
                ease: "power1.out",
            }, "-=0.5");

            tlOpen.call(function() {
                viewModulesButton.style.pointerEvents = 'auto';
                viewModulesButton.style.opacity = '';
            });

        }, 100);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const questions = document.querySelectorAll('.quiz-question');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitContainer = document.getElementById('submit-container');
    let currentQuestion = 0;

    function showQuestion(index) {
        questions[currentQuestion].style.display = 'none';
        questions[index].style.display = 'block';
        currentQuestion = index;

        prevBtn.disabled = currentQuestion === 0;
        nextBtn.style.display = currentQuestion === questions.length - 1 ? 'none' : 'inline-block';
        submitContainer.style.display = currentQuestion === questions.length - 1 ? 'inline-block' : 'none';
    }

    prevBtn.addEventListener('click', function() {
        if (currentQuestion > 0) {
            showQuestion(currentQuestion - 1);
        }
    });

    nextBtn.addEventListener('click', function() {
        if (currentQuestion < questions.length - 1) {
            showQuestion(currentQuestion + 1);
        }
    });
});