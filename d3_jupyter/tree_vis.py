d3_code_template = """
// 创建树状结构数据
var treeData = {{data}};

// 创建d3树布局
var margin = { top: 20, right: 90, bottom: 30, left: 90 },
  width = 960 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;

var svg = d3
  .select("#tree")
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var treemap = d3.tree().size([height, width]);

var nodes = d3.hierarchy(treeData);
nodes = treemap(nodes);

var link = svg
  .selectAll(".link")
  .data(nodes.descendants().slice(1))
  .enter()
  .append("path")
  .attr("class", "link")
  .attr("d", function (d) {
    return (
      "M" + d.y + "," + d.x +
      "C" + (d.y + d.parent.y) / 2 + "," + d.x +
      " " + (d.y + d.parent.y) / 2 + "," + d.parent.x +
      " " + d.parent.y + "," + d.parent.x
    );
  });

var node = svg
  .selectAll(".node")
  .data(nodes.descendants())
  .enter()
  .append("g")
  .attr("class", function (d) {
    return "node" + (d.children ? " node--internal" : " node--leaf");
  })
  .attr("transform", function (d) {
    return "translate(" + d.y + "," + d.x + ")";
  });

node.append("circle").attr("r", 10);

node
  .append("text")
  .attr("dy", ".35em")
  .attr("x", function (d) {
    return d.children ? -13 : 13;
  })
  .style("text-anchor", function (d) {
    return d.children ? "end" : "start";
  })
  .text(function (d) {
    return d.data.name;
  });
"""

html_template = """
<style>
.node circle {
  fill: #fff;
  stroke: steelblue;
  stroke-width: 1.5px;
}

.node text {
  font: 12px sans-serif;
}

.link {
  fill: none;
  stroke: #ccc;
  stroke-width: 1.5px;
}
</style>

<svg id="tree" width="960" height="500"></svg>

<script src="https://d3js.org/d3.v5.min.js"></script>

<script>
// 在这里插入d3.js代码
</script>
"""

from IPython.display import display, HTML

def display_tree_data(tree_data):
    d3_code = d3_code_template.replace(r'{{data}}', str(tree_data)) 

    html_content = html_template.replace("// 在这里插入d3.js代码", d3_code)
    return display(HTML(html_content))
