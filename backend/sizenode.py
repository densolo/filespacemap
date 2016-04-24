
class SizeNode:

    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.name2childs = {}

    def __str__(self):
        return "TreeNode(%s: %d bytes, %d items)" % (self.name, self.size, len(self.name2childs))

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def build_tree(path_sizes):
        root = SizeNode(None)
        for path, size in path_sizes:
            node = root.ensure_node(path)
            node.size = size
        return root

    def find_node(self, path):
        items = path.strip("/").split("/")
        node = self
        for i, it in enumerate(items):
            try:
                node = node.name2childs[it]
            except KeyError:
                raise KeyError("Child '%s' not found in %s (current path: %s)" % (it, self.name, '/'.join(items[:i])))
        return node

    def ensure_node(self, path):
        #print "ensure_node: %s" % path
        items = path.strip("/").split("/")
        node = self
        for it in items:
            node = node.name2childs.setdefault(it, SizeNode(it))
        return node
