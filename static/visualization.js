function createChart(visualizationData) {
    console.log("Visualization data:", visualizationData);
    anychart.onDocumentReady(function () {
        var chart = anychart.graph(visualizationData);
        chart.edges().arrows().enabled(true);
        chart.nodes().labels().enabled(true).format("{%name}" + " , " + "{%kind}" + " , " + "ID=(" + "{%id}" + ")").fontSize(12).fontWeight(600);
        chart.tooltip().useHtml(true);
        chart.nodes().tooltip().format("{%name}");
        chart.edges().tooltip().format("{%kind}" + ": " + "{%from}" +" -> " + "{%kind}" + ": " + "{%to}");



        // Node click event handler
        chart.listen("click", function(e) {
            var tag = e.domTarget.tag;
            if (tag) {
                if (tag.type === 'node') {
                    console.log("Node clicked:", tag);
                    var update = tag.id
                    console.log("Update:", update)
                    var forFunction = update - 1;
                    var node = visualizationData.nodes[forFunction];
                    updateInfoPanel(node);
                }
            }
            else {
                console.log("No node clicked");
            }
        });

        chart.container('chart_container');
        chart.draw();
        console.log("Chart created successfully");
    });
}

function getData(update){

}

function updateInfoPanel(node) {
    console.log("updateInfoPanel called with node:", node);
    var infoPanel = document.getElementById('infoPanel');
    var data = node;
    console.log("Node data:", data);
    var content = `<div class="pb-5">
                        <strong>${data.kind}: ${data.name}</strong><br>`;

    if (data.kind === "Employer") {
        content += `Address: ${data.headquarters_address}<br>
                    Start Date: ${data.start_date}<br>
                    End Date: ${data.end_date || 'Active'}<br>`;
        if (data.description) {
            content += `Description: ${data.description}`;
        }
    } else if (data.kind === "Employee") {
        content += `Email: ${data.email_address}<br>
                    Phone: ${data.phone_number}<br>
                    Address: ${data.employee_address}`;
    } else if (data.kind === "Institution") {
        content += `Institution Name: ${data.institution_name}`;
    }
    content += `</div>`;

    infoPanel.innerHTML = content;
    console.log("infoPanel content updated:", content);
}
