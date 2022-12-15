import argparse

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

    contain_count = 0
    overlap_count = 0

    for line in args.input:
        line = line.strip()
        pair = line.split(",")
        pair1 = pair[0].split("-")
        pair2 = pair[1].split("-")
        pair1_start = int(pair1[0])
        pair1_end = int(pair1[1])
        pair2_start = int(pair2[0])
        pair2_end = int(pair2[1])
        if pair1_start == pair2_start:
            contain_count += 1
        elif pair1_start < pair2_start:
            if pair2_end <= pair1_end:
                contain_count += 1
        else:
            if pair1_end <= pair2_end:
                contain_count += 1
        
        #PART B
        if not(pair1_start > pair2_end or pair1_end < pair2_start):
            overlap_count += 1

    print("Contain count: {}".format(contain_count))
    print("Overlap count: {}".format(overlap_count))

if __name__ == "__main__":
    main()