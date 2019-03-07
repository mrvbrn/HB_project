// instantiate the chart

var width = 1000,
    height = 1000,
    padding = 1.5, // separation between same-color nodes
    clusterPadding = 6
    maxRadius = 12; 

var data = getDataForRankingVisualization();

var simulation = d3.forceSimulation(data)
 .force("charge", d3.forceManyBody().strength([-800]))
 .force("x", d3.forceX())
 .force("y", d3.forceY())
 .on("tick", ticked);

function ticked(e) {
    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
}

var colorCircles = d3.scaleOrdinal(d3.schemeCategory20);

var scaleRadius = d3.scaleLinear()
            .domain([d3.min(data, function(d) { return +d.rank; }),
                    d3.max(data, function(d) { return +d.rank; })])
            .range([80, 30]);

var tooltip = d3.select("body")
 .append("div")
 .style("position", "absolute")
 .style("visibility", "hidden")
 .style("color", "white")
 .style("padding", "8px")
 .style("background-color", "#626D71")
 .style("border-radius", "6px")
 .style("text-align", "center")
 .style("font-family", "monospace")
 .style("width", "400px")
 .text("");



let svgContainer = d3.select("body")
                     .append("svg")
                     .attr("width", width)
                     .attr("height", height)
             
var node = svgContainer.selectAll("circle")
              .data(data)
              .enter()
              .append("g")
              .attr('transform', function(d) { return 'translate(' + d.x + ',' + d.y + ')'});

    
    node.append('circle')  
          .attr('r', function(d) { return scaleRadius(d.rank)})
          .style("fill", function(d) { return colorCircles(d.name)})
          .attr('transform', 'translate(' + [1000 / 2, 1000 / 2] + ')')
          .on("mouseover", function(d) {
               tooltip.html("rank = "+d.rank+"<br/>"+"average rating = "+d.rating+"<br/>");
               return tooltip.style("visibility", "visible");
          })
          .on("mousemove", function(){
              return tooltip.style("top", (d3.event.pageY-       10)+"px").style("left",(d3.event.pageX+10)+"px");
          })

    node.append("text")
            .attr("x", 75)
            .attr("y", 75)
            .attr("dy", "0.35em")
            .style("text-anchor", "middle")
            .text(function(d) { return d.name; } )
              
  