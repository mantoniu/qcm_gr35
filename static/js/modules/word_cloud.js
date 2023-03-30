var fill = d3.scaleOrdinal()
.range(d3.schemeCategory20)

var data = [
    {text: "Hello", value:4260},
    {text: "happy", value:5370},
    {text: "beautiful", value:2480},
    {text: "rainbow", value:4350},
    {text: "unicorn", value:1250},
    {text: "glitter", value:3140},
    {text: "happy", value:990},
    {text: "pie", value:4230}];

var layout = d3.layout.cloud()
    .size([400, 500])
    .words(data)
    .on("end", draw);


function draw(words) {
    d3.select("#cloud_word")
        .append("g")
        .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .text((d) => d.text)
        .style("font-size", (d) => d.size + "px")
        .style("font-family", (d) => d.font)
        .style("fill", (d, i) => fill(i))
        .attr("text-anchor", "middle")
        .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")");
}