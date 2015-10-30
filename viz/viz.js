var width=640;
var height=480;

var nodes = [];
var links = [];

console.log("Working");

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);


var link = svg.selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link");

var node = svg.selectAll('.node')
    .data(nodes)
    .enter().append('circle')
    .attr('class', 'node');

queue()
    .defer(d3.csv, "data/test.csv")
    .await(analyze);

function analyze(error, data) {
    console.log(data[0]);
    var src_idx = 0;
    var dst_idx = 0;
    console.log("Parsing csv: " + data.length);
    data.forEach(function(d) {
        src_idx = nodes.push(d.domain) - 1;
        dst_idx = nodes.push(d.type) - 1;
        console.log("Nodes: " + src_idx + ", " + dst_idx);
        links.push({source:src_idx, target:dst_idx});
    });
}

var force = d3.layout.force().size([width, height])
    .nodes(nodes)
    .links(links);

force.on("end", function() {
    console.log("Force End");
    node.attr('r', width/25)
        .attr('cx', function(d) { return d.x; })
        .attr('cy', function(d) { return d.y; });
     link.attr('x1', function(d) { return d.source.x; })
         .attr('y1', function(d) { return d.source.y; })
         .attr('x2', function(d) { return d.target.x; })
         .attr('y2', function(d) { return d.target.y; });
});

console.log("Force Start");
force.start();
