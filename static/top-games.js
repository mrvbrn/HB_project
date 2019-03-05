// instantiate the chart
var bubbleChart = function () {
    var width = 1000;
    var height = 400;
    function chart(selection){
        // we gonna get here
    }

    chart.width = function(value) {
        if (!arguments.length) { return width; }
        width = value;

        return chart;
    }
    chart.height = function(value) {
        if (!arguments.length) { return height; }
        height = value;

        return chart;
    }

    return chart;
  }

var data = getDataForRankingVisualization();

var simulation = d3.forceSimulation(data)
 .force("charge", d3.forceManyBody().strength([-350]))
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
            .range([50, 5]);

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
                     .attr("width", 800)
                     .attr("height", 1000);

var node = svgContainer.selectAll("circle")
              .data(data)
              .enter()
              .append("circle")
              .attr('r', function(d) { return scaleRadius(d.rank)})
              .style("fill", function(d) { return colorCircles(d.name)})
              .attr('transform', 'translate(' + [800 / 2, 1000 / 2] + ')')
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
            .text(function(d) { return d.name } );