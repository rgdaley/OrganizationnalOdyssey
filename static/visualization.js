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
    var content = `<div class="pb-5">
                        <strong>${data.type}: ${data.name}</strong><br>`;

    if (data.type === "Employer") {
        content += `Address: ${data.headquarters_address}<br>
                    Start Date: ${data.start_date}<br>
                    End Date: ${data.end_date || 'Active'}<br>`;
        if (data.description) {
            content += `Description: ${data.description}`;
        }
    } else if (data.type === "Employee") {
        content += `Email: ${data.email_address}<br>
                    Phone: ${data.phone_number}<br>
                    Address: ${data.employee_address}<br>
                    Employment Records:<br>`;
        data.employers.forEach(function(record) {
            content += `- Employer: ${record.employer}<br>
                        Job Title: ${record.jobTitle}<br>
                        Start Date: ${record.startDate}<br>
                        End Date: ${record.endDate || 'Active'}<br><br>`;
        });
    } else if (data.type === "Institution") {
        content += `Institution Name: ${data.institution_name}<br>
                    Certifications Granted:<br>`;
        data.certifications.forEach(function(cert) {
            content += `- Certification: ${cert.certificationName}<br>
                        Awarded To: ${cert.awardedTo}<br>
                        Award Date: ${cert.awardDate}<br><br>`;
        });
    }
    content += `</div>`;

    infoPanel.innerHTML = content;
}
