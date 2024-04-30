import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np


def transform_bbox_to_ax(bbox, img_bound, img_wh):
    img_w, img_h = img_wh  # 图片的真实宽高
    # bbox是相对图片左上角点的图片像素偏移，转换成相对左下角点的偏移
    bbox = [bbox[0], img_h - bbox[1], bbox[2], img_h - bbox[3]]

    # scale to normalized coord
    scale_factor = np.array([1 / img_w, 1/ img_h] * 2)
    sbbox = np.array(bbox) * scale_factor  # scale to [0, 1]
    
    # ax_im_x1, ax_im_y1是图片左下角点在绘图坐标系的中的坐标
    ax_im_x1, ax_im_y1, ax_im_w, ax_im_h = img_bound
    sbbox = sbbox * np.array([ax_im_w, ax_im_h, ax_im_w, ax_im_h]) + np.array([ax_im_x1, ax_im_y1, ax_im_x1, ax_im_y1])
    return sbbox

def min_cover_bbox(boxa, boxb):
    ax1, ay1, ax2, ay2 = boxa
    bx1, by1, bx2, by2 = boxb
    x1, y1 = min(ax1, bx1), min(ay1, by1)
    x2, y2 = max(ax2, bx2), max(ay2, by2)
    return [x1, y1, x2, y2]


def draw_node(ax, node, xy=(0, 0), scale_xy=(1.0, 1.0), sep=(0.5, 1.0)):
    """
    ax坐标系是左下角为原点，图片坐标系是左上角为原点，这点不太一样。
    
    xy: 是根节点的左下角点在ax坐标系中的位置
    scale_xy： 是全图缩放比例

    不考虑scale的情况下，每张图片的大小被放到ax坐标系一个1*1的格子里
    sep: 水平和垂直方向上，两个节点的间隔是多少（单位是scale_xy*1）
    """
    if isinstance(scale_xy, (float, int)):
        scale_xy = (scale_xy, scale_xy)
    if isinstance(sep, (float, int)):
        sep = (sep, sep)
    horizontal_sep, vertical_sep = sep   # 水平和垂直方向上，两个节点的间隔是多少倍的图片大小
    im_x1, im_y1 = xy
    
    text, img, children = node['text'], node.get('image', None), node.get('children', [])

    node_scale = node.get('scale', 1.0)
    if isinstance(node_scale, (float, int)):
        node_scale = (node_scale, node_scale)
    text_sep = node.get('text_sep', 0.1)

    # 绘制节点的图片
    if img is not None:
        im = Image.open(img) if isinstance(img, str) else img
        bbox = node.get('bbox_of_parent', None)
        if bbox is not None and node.get('need_crop', True):
            im = im.crop(bbox)
            
        # 1表示不考虑缩放的情况下，图片被放在1*1的格子里
        im_x2, im_y2 = im_x1 + 1 * scale_xy[0] * node_scale[0], im_y1 + 1 * scale_xy[1] * node_scale[1]  
        ax.imshow(im, aspect='equal', extent=(im_x1, im_x2, im_y1, im_y2))
    
    # 绘制文本描述框
    ax.text(xy[0] + scale_xy[0] * node_scale[0] / 2, xy[1] + scale_xy[1] * (node_scale[1] + text_sep), text, ha='center', va='bottom')

    # 当前节点在ax坐标系的范围 左下角点和
    im_bound_xywh = [im_x1, im_y1, scale_xy[0]*node_scale[0], scale_xy[1]*node_scale[1]]
    im_bound_xyxy = [im_x1, im_y1, im_x1+im_bound_xywh[2], im_y1+im_bound_xywh[3]]
    total_im_bound = [im_x1, im_y1, im_x1+scale_xy[0]*node_scale[0], im_y1+scale_xy[1] * (node_scale[1] + text_sep)]
    # 处理子节点
    for i, child in enumerate(children):
        # 计算子节点的左下角坐标
        child_xy = (
            im_x1 + i * scale_xy[0] * (1*node_scale[0]+horizontal_sep), 
            im_y1 - scale_xy[1] * (1*node_scale[1]+vertical_sep))     # 左下角点(x1, y1)
        
        # 在父节点中绘制红框
        bbox = child.get('bbox_of_parent', None)
        if bbox is not None:
            sbbox = transform_bbox_to_ax(bbox, im_bound_xywh, im.size)
            parent_rect = patches.Rectangle(sbbox[:2], sbbox[2]-sbbox[0], sbbox[3]-sbbox[1], linewidth=2, edgecolor='red', facecolor='none')
            ax.add_patch(parent_rect)
        else:
            sbbox = im_bound_xyxy
        
        # 绘制连接线
        parent_region_xy = ((sbbox[0] + sbbox[2]) / 2, (sbbox[1] + sbbox[3]) /2)
        child_head_xy = (child_xy[0] + scale_xy[0] / 2, child_xy[1]+scale_xy[1]*1.1)            # (x1, y1)  => ((x1+x2)/2, y2) = (x1+w/2, y1+h)
        ax.plot([parent_region_xy[0], child_head_xy[0]], [parent_region_xy[1], child_head_xy[1]], 'k-')
        
        # 递归绘制子节点
        child_total_im_bound = draw_node(ax, child, child_xy, scale_xy=(scale_xy[0], scale_xy[1]))
        total_im_bound = min_cover_bbox(total_im_bound, child_total_im_bound)
          
    return total_im_bound

def plot_tree_data(tree_data, xy=(0, 0), scale_xy=(1.0, 1.0), sep=(0.5, 1.0)):
    fig, ax = plt.subplots()
    total_bound = draw_node(ax, tree_data, xy=xy, scale_xy=scale_xy, sep=sep)
    print(total_bound)
    ax.set_xlim(total_bound[0], total_bound[2])
    ax.set_ylim(total_bound[1], total_bound[3])
    return fig, ax

# 示例数据


if __name__ == '__main__':

    tree_data = {
        "text": "root",
        "image": "../test_data/tree/img1.jpg",
        "scale": 2.0,
        "text_sep": 0.1,
        "children": [
            {
                "text": "child1",
                "image": "../test_data/tree/img1.jpg",
                "bbox_of_parent": [50, 50, 150, 150],  # 从根节点图片中裁剪区域
                "need_crop": True,
            },
            {
                "text": "child2",
                "image": "../test_data/tree/img1.jpg",
                "bbox_of_parent": [100, 150, 250, 200]  # 从根节点图片中裁剪区域
            },
            {
                "text": "xxx",
            }
        ]
    }

    plot_tree_data(tree_data)
