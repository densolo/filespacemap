
import os
import sys
import json
import stat

#sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    from_path = os.path.expanduser("~/")
    filestat_file = os.path.join(os.path.dirname(__file__), 'filestat.lst')
    dirstat_file = os.path.join(os.path.dirname(__file__), 'dirstat.lst')

    #scan_file_stat(from_path, stat_file)
    dir2size = calc_dir_stat(filestat_file, dirstat_file)

    root = Node(None)
    for path, size in dir2size.iteritems():
        node = root.ensure_node(path)
        node.size = size

    node = root.find_node(from_path)
    rects = square_node(node, 0., 0., 700., 400.)
    print 'rects', rects

    j = to_json(node.name2childs.values())
    print j
    f = open('data.json', 'w')
    data = json.dumps(j, indent=4)
    f.write(data)
    f.close()


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


def square_node(node, x, y, width, height):
    childs = sorted([c for c in node.name2childs.values()], key=lambda c: c.size, reverse=True)

    childs = [c for c in childs if c.size]

    for c in childs:
        print "  %s" % c

    sizes = [c.size for c in childs]

    sizes = normalize_sizes(sizes, width, height)

    # returns a list of rectangles
    rects = squarify(sizes, x, y, width, height)

    # padded rectangles will probably visualize better for certain cases
    #padded_rects = padded_squarify(sizes, x, y, width, height)
    return rects



class Node:

    def __init__(self, name):
        self.name = name
        self.size = 0
        self.name2childs = {}

    def __str__(self):
        return "Node(%s: %d bytes, %d items)" % (self.name, self.size, len(self.name2childs))

    def __repr__(self):
        return self.__str__()

    def find_node(self, path):
        items = path.strip("/").split("/")
        node = self
        for i, it in enumerate(items):
            try:
                node = node.name2childs[it]
            except KeyError:
                raise KeyError("Child '%s' not found in %s" % (it, '/'.join(items[:i])))
        return node

    def ensure_node(self, path):
        items = path.strip("/").split("/")
        node = self
        for it in items:
            node = node.name2childs.setdefault(it, Node(it))
        return node



def scan_file_stat(from_path, stat_file):
    f = open(stat_file, 'w')
    try:
        for path, size in iter_size(from_path):
            f.write("%s: %s\n" % (path, size))
    finally:
        f.close()
    #print 'main'


def calc_dir_stat(filestat_file, dirstat_file):
    lines = open(filestat_file, 'r').read(-1).splitlines()

    dir2size = {}
    for i, line in enumerate(lines):
        filepath, _sep, size = line.partition(":")
        if not filepath or not size:
            continue

        try:
            size = int(size.strip())
        except ValueError:
            continue

        dirpath = os.path.dirname(filepath)
        while dirpath:
            try:
                dir2size[dirpath] += size
            except KeyError:
                dir2size[dirpath] = size
            dirpath = dirpath.rpartition("/")[0]

    f = open(dirstat_file, 'w')
    try:
        for dirpath, size in sorted(dir2size.iteritems()):
            f.write("%s: %s\n" % (dirpath, size))
    finally:
        f.close()

    return dir2size



def iter_size(from_path):
    for root, dirs, files in os.walk(from_path):
        for f in files:
            path = os.path.join(root, f)
            st = os.lstat(path)
            if not stat.S_ISLNK(st.st_mode):
                yield path, st.st_size



# Squarified Treemap Layout
# Implements algorithm from Bruls, Huizing, van Wijk, "Squarified Treemaps"
#   (but not using their pseudocode)

def normalize_sizes(sizes, dx, dy):
    total_size = sum(sizes)
    total_area = dx * dy
    sizes = map(float, sizes)
    sizes = map(lambda size: size * total_area / total_size, sizes)
    return sizes

def pad_rectangle(rect):
    if rect['dx'] > 2:
        rect['x'] += 1
        rect['dx'] -= 2
    if rect['dy'] > 2:
        rect['y'] += 1
        rect['dy'] -= 2

def layoutrow(sizes, x, y, dx, dy):
    # generate rects for each size in sizes
    # dx >= dy
    # they will fill up height dy, and width will be determined by their area
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    covered_area = sum(sizes)
    width = covered_area / dy
    rects = []
    for size in sizes:
        rects.append({'x': x, 'y': y, 'dx': width, 'dy': size / width})
        y += size / width
    return rects

def layoutcol(sizes, x, y, dx, dy):
    # generate rects for each size in sizes
    # dx < dy
    # they will fill up width dx, and height will be determined by their area
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    covered_area = sum(sizes)
    height = covered_area / dx
    rects = []
    for size in sizes:
        rects.append({'x': x, 'y': y, 'dx': size / height, 'dy': height})
        x += size / height
    return rects

def layout(sizes, x, y, dx, dy):
    return layoutrow(sizes, x, y, dx, dy) if dx >= dy else layoutcol(sizes, x, y, dx, dy)

def leftoverrow(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    width = covered_area / dy
    leftover_x = x + width
    leftover_y = y
    leftover_dx = dx - width
    leftover_dy = dy
    return (leftover_x, leftover_y, leftover_dx, leftover_dy)

def leftovercol(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    height = covered_area / dx
    leftover_x = x
    leftover_y = y + height
    leftover_dx = dx
    leftover_dy = dy - height
    return (leftover_x, leftover_y, leftover_dx, leftover_dy)

def leftover(sizes, x, y, dx, dy):
    return leftoverrow(sizes, x, y, dx, dy) if dx >= dy else leftovercol(sizes, x, y, dx, dy)

def worst_ratio(sizes, x, y, dx, dy):
    return max([max(rect['dx'] / rect['dy'], rect['dy'] / rect['dx']) for rect in layout(sizes, x, y, dx, dy)])

def squarify(sizes, x, y, dx, dy):
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    # or dx * dy == sum(sizes)
    # sizes should be sorted biggest to smallest
    sizes = map(float, sizes)

    if len(sizes) == 0:
        return []

    if len(sizes) == 1:
        return layout(sizes, x, y, dx, dy)

    # figure out where 'split' should be
    i = 1
    while i < len(sizes) and worst_ratio(sizes[:i], x, y, dx, dy) >= worst_ratio(sizes[:(i+1)], x, y, dx, dy):
        i += 1
    current = sizes[:i]
    remaining = sizes[i:]

    (leftover_x, leftover_y, leftover_dx, leftover_dy) = leftover(current, x, y, dx, dy)
    return layout(current, x, y, dx, dy) + \
            squarify(remaining, leftover_x, leftover_y, leftover_dx, leftover_dy)

def padded_squarify(sizes, x, y, dx, dy):
    rects = squarify(sizes, x, y, dx, dy)
    for rect in rects:
        pad_rectangle(rect)
    return rects


if __name__ == "__main__":
    main()
