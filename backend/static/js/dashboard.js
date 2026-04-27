async function loadDashboardMetrics() {
    try {
        const response = await fetch("/api/dashboard-metrics");
        const data = await response.json();

        const performanceCanvas = document.getElementById("performanceChart");
        if (performanceCanvas) {
            new Chart(performanceCanvas, {
                type: "bar",
                data: {
                    labels: data.modules,
                    datasets: [{
                        label: "Performance (%)",
                        data: data.scores,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        const typeCounts = {};
        data.types.forEach(type => {
            typeCounts[type] = (typeCounts[type] || 0) + 1;
        });

        const typeCanvas = document.getElementById("typeChart");
        if (typeCanvas) {
            new Chart(typeCanvas, {
                type: "doughnut",
                data: {
                    labels: Object.keys(typeCounts),
                    datasets: [{
                        data: Object.values(typeCounts),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    } catch (error) {
        console.error("Dashboard metrics failed to load:", error);
    }
}

function loadRecentPredictions() {
    document.getElementById("lastCrop").innerText =
        localStorage.getItem("lastCropPrediction") || "No prediction yet";

    document.getElementById("lastFertilizer").innerText =
        localStorage.getItem("lastFertilizerPrediction") || "No prediction yet";

    document.getElementById("lastYield").innerText =
        localStorage.getItem("lastYieldPrediction") || "No prediction yet";

    document.getElementById("lastIrrigation").innerText =
        localStorage.getItem("lastIrrigationPrediction") || "No prediction yet";
}

document.addEventListener("DOMContentLoaded", () => {
    loadDashboardMetrics();
    loadRecentPredictions();
});