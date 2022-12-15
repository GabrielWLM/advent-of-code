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

    pri_sum = 0
    pri_sum_B = 0
    counter = 0
    dict1 = {}
    dict2 = {}
    for line in args.input:
        line = line.strip()
        half = int(len(line) / 2)
        dict = {}
        first_h = line[:half]
        sec_h = line[half:]
        for char in first_h:
            dict[char] = 1
        for char in sec_h:
            if char in dict:
                pri = ord(char)
                if pri > 96:
                    pri_sum += pri - 96
                else: pri_sum += pri - 64 + 26
                break
        
        # PART B
        if counter % 3 == 0:
            dict1 = {}
            dict2 = {}
            for char in line:
                dict1[char] = 1
        elif counter % 3 == 1:
            for char in line:
                if char in dict1:
                    dict2[char] = 1
        elif counter % 3 == 2:
            for char in line:
                if char in dict2:
                    pri = ord(char)
                    if pri > 96:
                        pri_sum_B += pri - 96
                    else: pri_sum_B += pri - 64 + 26
                    break
        counter += 1

    print("Sum of priorities: {}".format(pri_sum))
    print("Sum of priorities_B: {}".format(pri_sum_B))

if __name__ == "__main__":
    main()