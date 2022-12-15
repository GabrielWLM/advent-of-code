import argparse
from math import inf

def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "input", nargs="?", default="-",
        metavar="INPUT_FILE", type=argparse.FileType("r"),
        help="path to the input file (read from stdin if omitted)")

    parser.add_argument(
        "output", nargs="?", default="-",
        metavar="OUTPUT_FILE", type=argparse.FileType("w"),
        help="path to the output file (write to stdout if omitted)")

    args = parser.parse_args()

    class Directory:
        def __init__(self, name, parent=None, size=0):
            self.name = name
            self.parent = parent
            self.size = size
            self.dirs = {}
            self.files = {}
        
        def addFile(self, file_name, file_size):
            self.files[file_name] = file_size
            curr = self
            while(curr is not None):
                curr.size += file_size
                curr = curr.parent

        def addDir(self, dir_name):
            dir = Directory(name=dir_name, parent=self, size=0)
            self.dirs[dir_name] = dir
            return dir

        def getDir(self, dir_name):
            if dir_name not in self.dirs:
                return self.addDir(dir_name)
            else:
                return self.dirs[dir_name]

    # Parse Input
    top_dir = Directory(name="/", parent=None, size=0)
    curr_dir = top_dir

    for line in args.input:
        text = line.split()
        if text[0] == "$":
            if text[1] == "cd":
                dir_name = text[2]
                if dir_name == "/":
                    curr_dir = top_dir
                elif dir_name == "..":
                    curr_dir = curr_dir.parent
                else:
                    curr_dir = curr_dir.getDir(dir_name)
        elif text[0] == "dir":
            dir_name = text[1]
            curr_dir.addDir(dir_name)
        else:
            file_size = int(text[0])
            file_name = text[1]
            curr_dir.addFile(file_name, file_size)

    # Search and add up directories with size <=100,000
    def recursive_get_sum(curr_dir):
        sum = 0
        if curr_dir.size <= 100000:
            sum += curr_dir.size
        if len(curr_dir.dirs) > 0:
            for dir in curr_dir.dirs.values():
                sum += recursive_get_sum(dir)
        return sum
    
    size_sum = recursive_get_sum(top_dir)

    print("Total size of directories: {}".format(size_sum))

    # PART TWO
    total_space = 70000000
    space_needed = 30000000
    unused_space = total_space - top_dir.size
    add_space_needed = space_needed - unused_space # Assume add_space_needed>0

    def recursive_get_smallest_d(curr_dir):
        if curr_dir.size < add_space_needed:
            return inf
        
        curr_smallest = curr_dir.size
        if len(curr_dir.dirs) > 0:
            for dir in curr_dir.dirs.values():
                curr_smallest = min(curr_smallest, recursive_get_smallest_d(dir))
        return curr_smallest

    dir_size_tb_removed = recursive_get_smallest_d(top_dir)

    print("Size of directory to be deleted: {}".format(dir_size_tb_removed))

if __name__ == "__main__":
    main()