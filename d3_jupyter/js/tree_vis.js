// 获取键'key3'的值，如果不存在则返回600
function getValueOrDefault(dict, key, defaultValue = 600) {
     return dict[key] ?? defaultValue;
 }

// 创建树状结构数据
function run(){
var treeData = <<data>>;
var kwargs = <<kwargs>>;

var margin_ltrb = [kwargs.margin_left, kwargs.margin_top, kwargs.margin_right, kwargs.margin_bottom];  // left, top, right, bottom
var width = kwargs.width;    // 800
var height = kwargs.height   // 600
var image_width = kwargs.image_width
var image_height = kwargs.image_height

// 将数据转换为d3的tree形式数据
var treemap = d3.tree().size([height, width]);
var nodes = d3.hierarchy(treeData);
nodes = treemap(nodes);

// 获取画布，并在内部施加偏移
var svg = d3.select("#tree")
     .attr("width", width+margin_ltrb[0]+margin_ltrb[2])
     .attr("height", height+margin_ltrb[1]+margin_ltrb[3])
     .append("g").attr("transform", `translate(${margin_ltrb[0]}, ${margin_ltrb[1]})`);

// 绘制基本内容：node(g), link(path), 
// node(g) 包含 circle, text, img
var link = svg
  .selectAll(".link")
  .data(nodes.descendants().slice(1))   // 注入tree数据, slice1根节点不用绘制link
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

node
  .filter(function (d) {
    return d.data.image_path;
  })
  .append('g').attr('class', 'node node--leaf')
  .append("image")
  .attr("href", function (d) {
    return d.data.image_path;
  })
  .attr("x", -8)
  .attr("y", -8)
  .attr("width", 100)
  .attr("height", 100);

node.append("circle").attr("r", 10)
    .on("click", function(d) {
    const circle = d3.select(this);
    const currentRadius = parseFloat(circle.attr("r"));
    const newRadius = currentRadius === 10 ? 20 : 10; // 切换节点大小状态

    circle.attr("r", newRadius);
});

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

// d3.select("#tree_div").append('svg').selectAll("image").data(nodes.descendants()).enter()
//   .filter(function (d) {
//     return d.data.image_path;
//   })
//   .append('g').attr('class', 'node node--leaf')
//   .append("image")
//   .attr("href", function (d) {
//     return d.data.image_path;
//   })
//   .attr("x", -8)
//   .attr("y", -8)
//   .attr("width", 100)
//   .attr("height", 100);
}

run();
