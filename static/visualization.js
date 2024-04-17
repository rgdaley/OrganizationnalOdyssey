function createChart(data) {
    anychart.onDocumentReady(function() {
        var chart = anychart.graph(data);

        chart.nodes().labels().enabled(true);
        chart.nodes().labels().format("{%name}");
        chart.nodes().labels().fontSize(12);
        chart.nodes().labels().fontWeight(600);

        chart.edges().arrows().enabled(true);

        // Customize tooltip based on node and edge type
        chart.nodes().tooltip().format(function() {
            var info = "Name: " + this.name + "<br>Type: " + this.data.type;
            if (this.data.type === "Employer") {
                info += "<br>Address: " + this.data.address +
                        "<br>Start Date: " + this.data.start_date +
                        "<br>End Date: " + this.data.end_date;
            }
            return info;
        });
        chart.edges().tooltip().format(function() {
            return "Relation: " + this.data.type;
        });

        chart.container("chart_container");
        chart.draw();
    });
}
