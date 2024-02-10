// Example JavaScript code for rendering the graph
function renderGraph(visualizationData) {
    var graphContainer = document.getElementById('graph-container');

    // Render nodes
    visualizationData.nodes.forEach(function(node) {
        var nodeElement = document.createElement('div');
        nodeElement.className = 'node';
        var text = node.id;
        for (const attribute of node.attributes){
            text += "\n" + attribute;
        }
        nodeElement.textContent = text;
        graphContainer.appendChild(nodeElement);
    });

    // Render edges
    visualizationData.edges.forEach(function(edge) {
        var edgeElement = document.createElement('div');
        edgeElement.className = 'edge';
        graphContainer.appendChild(edgeElement);
    });
}