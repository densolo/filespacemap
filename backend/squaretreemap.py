
# SquareTreeMap
# Reuse of the squarify package by Uri Laserson
# that implements algorithm from Bruls, Huizing, van Wijk, "Squarified Treemaps"

import squarify


class SquareTreeMap:

    @staticmethod
    def squarify_size_nodes(path, nodes, x, y, width, height, min_size):
        # for n in nodes:
        #     print "%s -> %s" % (n.name, n.size)

        nodes = [n for n in nodes if n.size > min_size]
        nodes = sorted(nodes, key=lambda n: n.size, reverse=True)

        sizes = [n.size for n in nodes]
        sizes = squarify.normalize_sizes(sizes, width, height)
        rects = squarify.squarify(sizes, x, y, width, height)

        for i in range(len(rects)):
            rect = rects[i]
            node = nodes[i]
            child_path = path + "/" + node.name

            # print "[DEBUG] child_path", i, child_path, node.size
            # assert rect['x'] >= x, "%s (%s)" % (rect, (x, y, width, height))
            # assert rect['y'] >= y, "%s (%s)" % (rect, (x, y, width, height))
            # assert rect['dx'] <= width + 1, "%s (%s)" % (rect, (x, y, width, height))
            # assert rect['dy'] <= height + 1, "%s (%s)" % (rect, (x, y, width, height))

            rect['name'] = node.name
            rect['path'] = child_path

            child_rects = SquareTreeMap.squarify_size_nodes(
                child_path, node.name2childs.values(), rect['x'], rect['y'], rect['dx'], rect['dy'], min_size)
            rects.extend(child_rects)

        return rects
