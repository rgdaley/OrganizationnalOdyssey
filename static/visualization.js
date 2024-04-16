document.addEventListener("DOMContentLoaded", function () {
    fetchAndCreateChart();
});

function fetchAndCreateChart() {
    fetch('/visualize')
        .then(response => response.json())
        .then(data => {
            anychart.onDocumentReady(function () {
                var chart = anychart.graph({
                    nodes: data.nodes,
                    edges: data.links
                });
                chart.container('chart_container');
                chart.draw();
            });
        })
        .catch(error => console.error('Error loading visualization data:', error));
}
