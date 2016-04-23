
import os
import sys

test_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(test_root, "..", "backend"))


import unittest


class SpaceStatTests(unittest.TestCase):

    def test_01_file_util(self):
        from fileutil import FileUtil

        test_file = __file__ + ".test_01.data"
        path_sizes = [
            ("path1", 1),
            ("path2", 2),
            ("path3", 3),
        ]

        iter_lines = FileUtil.combine_path_sizes(path_sizes)
        FileUtil.write_all(test_file, iter_lines)

        data = FileUtil.read_all(test_file)
        self.assertEqual("""
path1: 1
path2: 2
path3: 3
        """.strip(), data.strip())

        path2size = dict([(path, size) for path, size in FileUtil.parse_path_sizes(data.splitlines())])
        self.assertEqual(path2size['path2'], 2)

    def test_02_size_tree(self):
        from fileutil import FileUtil
        from sizenode import SizeNode

        lines = """\
node_modules/promise/domains: 15908
node_modules/promise/lib: 15912
node_modules/promise/node_modules: 34383
node_modules/promise/node_modules/asap: 34383
node_modules/promise/setimmediate: 15886
node_modules/promise/src: 16314
""".splitlines()

        path_sizes = FileUtil.parse_path_sizes(lines)
        self.assertEqual(len([ps for ps in path_sizes]), 6)

        path_sizes = FileUtil.parse_path_sizes(lines)
        tree = SizeNode.build_tree(path_sizes)
        self.assertTrue(tree)
        self.assertTrue(tree.name2childs)
        self.assertEqual(tree.find_node("node_modules/promise/node_modules/asap").size, 34383)
