
import os
import sys
import json
import stat
import types

#sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fileutil import FileUtil
from sizenode import SizeNode
from squaretreemap import SquareTreeMap


def main():
    from_path = os.path.expanduser(sys.argv[1])

    filestat_file = os.path.join(os.path.dirname(__file__), '../data/filestat.lst')
    dirstat_file = os.path.join(os.path.dirname(__file__), '../data/dirstat.lst')
    json_file = os.path.join(os.path.dirname(__file__), '../data/data.json')

    #scan_file_sizes(from_path, stat_file)
    #calc_dir_sizes(filestat_file, dirstat_file)

    lines = FileUtil.read_all(dirstat_file).splitlines()
    iter_dir_sizes = FileUtil.parse_path_sizes(lines)

    root = SizeNode.build_tree(iter_dir_sizes)

    node = root.find_node(os.path.join(from_path))

    #nodes = sorted([c for c in node.name2childs.values()], key=lambda n: n.size, reverse=True)
    nodes = node.name2childs.values()
    min_size = node.size * 0.001
    #print "min_size", min_size

    #nodes = SquareTreeMap.norm_node_sizes(nodes)
    rects = SquareTreeMap.squarify_size_nodes(node.name, nodes, 0., 0., 700., 400., min_size)

    # rects = square_node(node, 0., 0., 700., 400.)
    # print 'rects', rects
    write_d3_rect_json(json_file, rects)


def write_d3_rect_json(json_file, rects):
    data = json.dumps(rects, indent=4)
    FileUtil.write_all(json_file, data)


def write_d3_treemap_json(json_file, node):
    j = to_json(node.name2childs.values())
    data = json.dumps(j, indent=4)
    FileUtil.write_all(json_file, data)


def to_json(nodes):
    return {
        "name": "",
        "children": [
            {
                "name": c.name,
                "size": c.size
            } for c in nodes
        ]
    }


def scan_file_sizes(from_path, stat_file):
    iter_path_sizes = FileUtil.walk_path_sizes(from_path)
    iter_lines = FileUtil.combine_path_sizes(iter_path_sizes)
    FileUtil.write_all(stat_file, iter_lines)


def calc_dir_sizes(filestat_file, dirstat_file):
    lines = FileUtil.read_all(filestat_file).splitlines()

    dir2size = {}
    for filepath, size in FileUtil.parse_path_sizes(lines):
        dir2size[filepath] = size
        dirpath = os.path.dirname(filepath)
        while dirpath:
            try:
                dir2size[dirpath] += size
            except KeyError:
                dir2size[dirpath] = size
            dirpath = dirpath.rpartition("/")[0]

    iter_lines = FileUtil.combine_path_sizes(sorted(dir2size.items()))
    FileUtil.write_all(dirstat_file, iter_lines)


if __name__ == "__main__":
    main()
