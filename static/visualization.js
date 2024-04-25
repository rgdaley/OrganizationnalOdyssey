function createChart(visualizationData) {
    anychart.onDocumentReady(function () {
        var chart = anychart.graph(visualizationData);
        chart.edges().arrows().enabled(true);
        chart.nodes().labels().enabled(true).format("{%name}").fontSize(12).fontWeight(600);

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
    var label = "";
        if (node.type === "Employer") {
            label = node.name;
        } else if (node.type === "Employee") {
            label = node.name;
        } else if (node.type === "Institution") {
            label = node.name;
        }
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

function showNodeInfo(node) {
    var info = "";
    if (node.type === "Employer") {
        info = "<h2>" + node.name + "</h2>" +
               "<p><strong>Start Date:</strong> " + node.start_date + "</p>" +
               "<p><strong>End Date:</strong> " + node.end_date + "</p>" +
               "<p><strong>Description:</strong> " + node.description + "</p>";
    } else if (node.type === "Employee") {
        info = "<h2>" + node.name + "</h2>" +
               "<p><strong>Phone Number:</strong> " + node.phone_number + "</p>" +
               "<p><strong>Email Address:</strong> " + node.email_address + "</p>" +
               "<p><strong>Address:</strong> " + node.address + "</p>";
    } else if (node.type === "Institution") {
        info = "<h2>" + node.name + "</h2>";
    }
    document.getElementById("infoPanel").innerHTML = info;
}