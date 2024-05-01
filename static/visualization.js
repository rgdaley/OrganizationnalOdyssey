function createChart(visualizationData) {
    console.log("Visualization data:", visualizationData);
    anychart.onDocumentReady(function () {
        var chart = anychart.graph(visualizationData);
        chart.edges().arrows().enabled(true);
        chart.nodes().labels().enabled(true).format("{%name}" + " , " + "{%kind}" + " , " + "ID=(" + "{%id}" + ")").fontSize(12).fontWeight(600);
        chart.tooltip().useHtml(true);
        chart.nodes().tooltip().format("{%name}");
        chart.edges().tooltip().format("Parent: {%from} -> Child: {%to} ({%kind})");



        // Node click event handler
        chart.listen("click", function(e) {
            var tag = e.domTarget.tag;
            if (tag && tag.type === 'node') {
                console.log("Node clicked:", tag);
                var node = visualizationData.nodes.find(node => node.id == tag.id);
                console.log("Found Node:", node);
                if (node) {
                    updateInfoPanel(node);
                } else {
                    console.log("Node not found for ID:", tag.id);
                }
            } else {
                console.log("No node clicked or non-node element clicked");
            }
        });


        chart.container('chart_container');
        chart.draw();
        console.log("Chart created successfully");
    });
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
    } 
    content += `</div>`;

    infoPanel.innerHTML = content;
    console.log("infoPanel content updated:", content);
}
