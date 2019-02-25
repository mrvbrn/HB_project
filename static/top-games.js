// instantiate the chart
var bubbleChart = function () {
    var width = 1500;
    var height = 400;
    function chart(selection, data){
      svgContainer = selection.select('svg');
      svgContainer.attr('width', width).attr('height', height);

      var tooltip = selection
       .append("div")
       .style("position", "absolute")
       .style("visibility", "hidden")
       .style("color", "black")
       .style("padding", "8px")
       .style("background-color", "#626D71")
       .style("border-radius", "6px")
       .style("text-align", "center")
       .style("font-family", "monospace")
       .style("width", "400px")
       .text("");

       var simulation = d3.forceSimulation(data)
        .force("charge", d3.forceManyBody().strength([-350]))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .on("tick", ticked);

       function ticked(e) {
           node.attr("cx", function(d) { return d.x; })
               .attr("cy", function(d) { return d.y; });
       }

       var colorCircles = d3.scaleOrdinal(d3.schemeCategory10);

       var scaleRadius = d3.scaleLinear()
                   .domain([d3.min(data, function(d) { return +d.rank; }),
                           d3.max(data, function(d) { return +d.rank; })])
                   .range([50, 5]);

      var node = svgContainer.selectAll("circle")
                     .data(data)
                     .enter()
                     .append("circle")
                     .attr('r', function(d) { return scaleRadius(d.rank)})
                     .style("fill", function(d) { return colorCircles(d.rank)})
                     .attr('transform', 'translate(' + [width / 2, height / 2] + ')')
                     .on("mouseover", function(d) {
                          tooltip.html("app name = " +d.name+"<br/>"+"rank = "+d.rank+"<br/>"+"average rating = "+d.rating+"<br/>");
                          return tooltip.style("visibility", "visible");
                     })
                     .on("mousemove", function(){
                         return tooltip.style("top", (d3.event.pageY-       10)+"px").style("left",(d3.event.pageX+10)+"px");
                     })
                     .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

    node.append("text")
      .attr("x", 75)
      .attr("y", 75)
      .attr("dy", "0.35em")
      .attr("font-size","1.8em")
      .attr("text-anchor", "middle")
      .text(function(d) { return d.name } );
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

var chart = bubbleChart();
chart(
  d3.select("#chart"),  // this refers to the div with id="chart" in top_games.html
  getDataForRankingVisualization(),
);
