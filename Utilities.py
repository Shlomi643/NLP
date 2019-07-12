from os import listdir
from os.path import isfile, join


class Data:
    filesMap = {}
    names = []

    def __init__(self):
        Data.init_map()

    @staticmethod
    def set_s(format_index, name):
        return 'First' if format_index == '1' \
                   else 'Second', open("Scripts/Format " + format_index + "/" + name + ".html").read()

    @staticmethod
    def build_map(path):
        my_dir = "Scripts/" + path
        files = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
        for f in files:
            file_name = f[0:f.index('.html')]
            Data.names.append(file_name)
            Data.filesMap[file_name] = Data.set_s(my_dir[-1], file_name)

    @staticmethod
    def init_map():
        Data.build_map("Format 1")
        Data.build_map("Format 2")

    @staticmethod
    def script(name):
        return Data.filesMap[name][1]

    @staticmethod
    def formatter(name):
        return Data.filesMap[name][0]

    @staticmethod
    def get_token(line):
        def rpl(y): return line.replace(y, ' ')
        for x in [',', '.', ';', '?', '!', '/']:
            line = rpl(x)
        return line.split()

