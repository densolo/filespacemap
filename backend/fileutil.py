
import os
import types


class FileUtil:

    @staticmethod
    def write_all(path, data, mode='w'):
        f = open(path, mode)
        try:
            if isinstance(data, (list, types.GeneratorType)):
                for chunk in data:
                    f.write(chunk)
            else:
                f.write(data)
        finally:
            f.close()

    @staticmethod
    def read_all(path):
        return open(path, 'r').read(-1)

    @staticmethod
    def walk_path_sizes(from_path):
        for root, dirs, files in os.walk(from_path):
            for f in files:
                path = os.path.join(root, f)
                st = os.lstat(path)
                if not stat.S_ISLNK(st.st_mode):
                    yield path, st.st_size

    @staticmethod
    def combine_path_sizes(iter):
        for path, size in iter:
            yield "%s: %s\n" % (path, size)

    @staticmethod
    def parse_path_sizes(lines):
        for i, line in enumerate(lines):
            path, _sep, size = line.rpartition(":")
            if not path or not size:
                continue

            try:
                size = int(size.strip())
            except ValueError:
                continue

            yield path, size
