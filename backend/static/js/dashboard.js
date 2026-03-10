
const nutrientCanvas = document.getElementById("nutrientChart");
if (nutrientCanvas) {
    new Chart(nutrientCanvas, {
        type: "bar",
        data: {
            labels: ["Nitrogen", "Phosphorus", "Potassium"],
            datasets: [{
                label: "Sample Nutrient Levels",
                data: [90, 42, 43],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

const predictionCanvas = document.getElementById("predictionChart");
if (predictionCanvas) {
    new Chart(predictionCanvas, {
        type: "doughnut",
        data: {
            labels: ["Crop", "Fertilizer", "Irrigation", "Yield"],
            datasets: [{
                label: "Module Distribution",
                data: [40, 20, 20, 20],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}