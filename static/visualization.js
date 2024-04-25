function createChart(visualizationData) {
    anychart.onDocumentReady(function () {
        var chart = anychart.graph(visualizationData);
        chart.edges().arrows().enabled(true);
        chart.nodes().labels().enabled(true).format("{%name}").fontSize(12).fontWeight(600);
        chart.tooltip().useHtml(true);
        chart.nodes().tooltip().format("{%name}");
        chart.edges().tooltip().format("{%from} -> {%to}");

        // Node click event handler
        chart.listen("click", function (e) {
            if (e.point) {
                updateInfoPanel(e.point);
            }
        });

        chart.container('chart_container');
        chart.draw();
    });
}

function updateInfoPanel(node) {
    var infoPanel = document.getElementById('infoPanel');
    var data = node.getData();
    var content = `<div class="pb-5">
                        <strong>${data.type}: ${data.name}</strong><br>`;

    if (data.type === "Employer") {
        content += `Address: ${data.address}<br>
                    Start Date: ${data.start_date}<br>
                    End Date: ${data.end_date || 'Active'}<br>`;
        if (data.description) {
            content += `Description: ${data.description}`;
        }
    } else if (data.type === "Employee") {
        content += `Email: ${data.email_address}<br>
                    Phone: ${data.phone_number}<br>
                    Address: ${data.address}`;
    } else if (data.type === "Institution") {
        content += `Institution Name: ${data.name}`;
    }
    content += `</div>`;

    infoPanel.innerHTML = content;
}
