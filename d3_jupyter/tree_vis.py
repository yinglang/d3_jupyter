import os.path as osp
d3_code_template = open(osp.join(osp.split(__file__)[0], 'js/tree_vis.js')).read()

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

.node image {
  pointer-events: none;
}

.link {
  fill: none;
  stroke: #ccc;
  stroke-width: 1.5px;
}

</style>

<div id="tree_div" width="auto" height="auto" style="overflow-x: scroll; overflow-y: scroll;">
  <svg id="tree"></svg>
</div>

<script src="https://d3js.org/d3.v5.min.js"></script>

<script>
// 在这里插入d3.js代码
</script>
"""

from IPython.display import display, HTML

def display_tree_data(tree_data, 
                      width=800, height=600, 
                      margin_left=50, margin_top=10, margin_right=50, margin_bottom=10,
                      image_width=100, image_height=100
                      ):
    d3_code = d3_code_template.replace(r'<<data>>', str(tree_data)) 
    
    kwargs = dict(
        width=width, height=height, 
        margin_left=margin_left, margin_top=margin_top, margin_right=margin_right, margin_bottom=margin_bottom,
        image_width=image_width, image_height=image_height,
        )
    d3_code = d3_code.replace(r'<<kwargs>>', str(kwargs))

    html_content = html_template.replace("// 在这里插入d3.js代码", d3_code)
    return display(HTML(html_content))
