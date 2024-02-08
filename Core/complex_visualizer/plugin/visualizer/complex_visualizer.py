import json
from Core.core.services.visualizing import VisualizingService
from django.template import engines


def contains_edge(edges, e):
    for edge in edges:
        if e == edge:
            return True
    return False


class ComplexVisualizer(VisualizingService):

    def id(self):
        return "complex_visualizer"

    def name(self):
        return "Complex Visualizer View"

    def visualize(self, graph, request):
        vertices = {}
        edges = []
        for vertex in graph.vertices:
            attributes = []
            for attribute in vertex.attributes.keys():
                attributes.append(attribute + ": " + str(vertex.attributes[attribute]))
            vertices[vertex.id] = {
                "id": "Vertex_" + str(vertex.id),
                "attributes": attributes
            }
            for edge in vertex.edges():
                current_edge = {"start": edge.get_start(), "end": edge.get_end()}
                if not contains_edge(edges, current_edge):
                    edges.append(current_edge)

        view = """
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

                <style>
                    .node {
                    cursor: pointer;
                    }

                    .link {
                    fill: none;
                    stroke: #9ecae1;
                    stroke-width: 1.5px;
                    }
                </style>

                <script>

                    var current = null;
                    
                    var verticesGraph = JSON.parse("{{vertices |escapejs}}");
                    var edgesGraph = JSON.parse("{{edges |escapejs}}");

                    edgesGraph.forEach(function(edge) {
                        link.source = verticesGraph[edge.start];
                        link.target = verticesGraph[edge.end];
                    });

                    function vertexOnClick(el) {

                        var text = "";
                        text += "ID:" + el.id + "\\n";
                        if(current != null) {
                            vertexDetails(verticesGraph[current.id.replace("VERTEX_", "")], '#003B73');
                        }
                        
                        var node = verticesGraph[el.id.replace("Vertex_", "")];
                        current = node;
                        vertexDetails(node, "red");
                        for(var i=0;i<node.attributes.length;i++) {
                            text += node.attributes[i] + "\\n";
                        }
                        id = el.id.replace("Vertex_", "");
                        const dynamicTreeContainer = document.getElementById('dynamic-tree');
                        const xhr = new XMLHttpRequest();
                        xhr.open('GET', `/${id};select`, true);
                        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                        xhr.onreadystatechange = function () {
                            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                                dynamicTreeContainer.innerHTML = xhr.responseText;

                                const newToggles = dynamicTreeContainer.querySelectorAll('.node-toggle');
                                newToggles.forEach(toggle => {
                                    toggle.addEventListener('click', function (event) {
                                        event.preventDefault();
                                        const newNode = this.parentNode;
                                        toggleNode(newNode);
                                    });
                                });
                                let nodesTree = document.querySelectorAll('.node-toggle');
                                nodesTree.forEach(toggle => {
                                    toggle.addEventListener('click', function (event) {
                                        event.preventDefault();
                                        const node = this.parentNode;
                                        let newSelected = node.querySelector("#object-id").innerHTML;
                                        if (current != null) {
                                            vertexDetails(current, "#003B73")
                                        }
                                        current = verticesGraph[newSelected];
                                        vertexDetails(current, "red");
                                    });
                                });
                                if (document.getElementById('last-opened-node') != null) {
                                    const lastOpenedNode = document.getElementById('last-opened-node').innerHTML;
                                    element = document.getElementById(lastOpenedNode);
                                    if (element) {
                                        scrollIfNeeded(element, document.getElementById('tree'));
                                        element.classList.add("selected-item");
                                    }
                                }
                            }
                        };
                        xhr.send();

                        alert(text);
                    }

                    var force = d3.layout.force() //kreiranje force layout-a
                        .size([1000, 450]) //raspoloziv prostor za iscrtavanje
                        .nodes(d3.values(verticesGraph)) //dodaj nodove
                        .links(edgesGraph) //dodaj linkove
                        .on("tick", tick) //sta treba da se desi kada su izracunate nove pozicija elemenata
                        .linkDistance(350) //razmak izmedju elemenata
                        .charge(-1500)//koliko da se elementi odbijaju
                        .gravity(0.75)
                        .start(); //pokreni izracunavanje pozicija

                    // add pan and zoom
                    var svg = d3.select('#mainView').call(d3.behavior.zoom().on("zoom", function () {
                            svg.attr("transform", " translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
                    })).append('g');

                    // add the links
                    var link = svg.selectAll('.link')
                        .data(edgesGraph)
                        .enter().append('line')
                        .attr('class', 'link');

                    // add the nodes
                    var node = svg.selectAll('.node')
                        .data(force.nodes()) //add
                        .enter().append('g')
                        .attr('class', 'node')
                        .attr('id', function(d){return d.id;})
                        .on('click',function(){
                        nodeClick(this);
                        });
                    d3.selectAll('.node').each(function(d){vertexDetails(d, '#003B73');});

                    function vertexDetails(vertex, color) {
                        var length = 10;
                        for(var i=0;i<vertex.attributes.length;i++) {
                            if(length<vertex.attributes[i].length) length = vertex.attributes[i].length
                        }

                        var attributesNum = vertex.attributes.length;

                        var textSize = 12;
                        var high = 30;
                        high += (attributesNum == 0) ? textSize: attributesNum*textSize;
                        var width = length * textSize/2 + 2*textSize + 5;
                        if (width > 265)
                            width = 265;

                        // add rectangle
                        d3.select("g#"+vertex.id).append('rect').
                            attr('x',0).attr('y',0).attr('width',width).attr('height',high)
                            .attr('fill', color);

                        // add id
                        d3.select("g#"+vertex.id).append('text').attr('x',width/2).attr('y',10)
                        .attr('text-anchor','middle')
                        .attr('font-size',textSize).attr('font-family','Poppins')
                        .attr('fill','white').text(vertex.id);

                        // add divider
                        d3.select("g#"+vertex.id).append('line').
                        attr('x1',0).attr('y1',textSize).attr('x2',width).attr('y2',textSize)
                        .attr('stroke','gray').attr('stroke-width',2);

                        // add attributes
                        for(var i=0;i<attributesNum;i++)
                        {   
                            let slice_attr = d.attributes[i].length;
                            if (slice_attr > 40)
                                slice_attr = 40;
                            d3.select("g#"+vertex.id).append('text').attr('x',0).attr('y',20+i*textSize)
                            .attr('text-anchor','start')
                            .attr('font-size',textSize).attr('font-family','Poppins')
                            .attr('fill','white').text(vertex.attributes[i].slice(0, slice_attr));
                        }
                    }

                    function tick(e) {
                        node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";})
                            .call(force.drag);

                        link.attr('x1', function(d) { return d.source.x; })
                            .attr('y1', function(d) { return d.source.y; })
                            .attr('x2', function(d) { return d.target.x; })
                            .attr('y2', function(d) { return d.target.y; });
                    }

                    init();
            
                    function init() {
                        let main = d3.select("#mainView").node();

                        let observer = new MutationObserver(observer_callback);

                        observer.observe(main, {
                            subtree: true,
                            attributes: true,
                            childList: true,
                            characterData: true
                        });
                    }

                    function observer_callback() {
                        let main = d3.select("#mainView").html();
                        d3.select("#birdView").html(main);

                        let mainWidth = d3.select("#mainView").select("g").node().getBBox().width;
                        let mainHeight = d3.select("#mainView").select("g").node().getBBox().height;

                        let birdWidth = $("#birdView")[0].clientWidth;
                        let birdHeight = $("#birdView")[0].clientHeight;

                        let scaleWidth = birdWidth / mainWidth;
                        let scaleHeight = birdHeight / mainHeight;

                        let scale = 0;
                        if(scaleWidth < scaleHeight){
                            scale = scaleWidth;
                        }else{
                            scale = scaleHeight;
                        }
                        
                        let x = d3.select("#birdView").select("g").node().getBBox().x;
                        let y = d3.select("#birdView").select("g").node().getBBox().y;
                        d3.select("#birdView").select('g').attr("transform", "translate ("+[-x*scale, -y*scale]+") scale("+ scale +")");
                    }
                </script>
               """
        django_eng = engines['django']
        html_view = django_eng.from_string(view)
        html_template = html_view.render({
            "vertices": json.dumps(vertices),
            "edges": json.dumps(edges)
        }, request)
        return html_template
