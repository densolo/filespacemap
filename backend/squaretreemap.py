
# SquareTreeMap
# Reuse of the squarify package by Uri Laserson
# that implements algorithm from Bruls, Huizing, van Wijk, "Squarified Treemaps"

import squarify


class SquareTreeMap:

    @staticmethod
    def squarify_size_nodes(nodes, x, y, width, height):
        nodes = [n for n in nodes if n.size]
        nodes = sorted(nodes, key=lambda n: n.size, reverse=True)

        sizes = [n.size for n in nodes]
        sizes = squarify.normalize_sizes(sizes, width - x, height - y)
        rects = squarify.squarify(sizes, x, y, width, height)

        for i, rect in enumerate(rects):
            rect['name'] = nodes[i].name

        return rects
