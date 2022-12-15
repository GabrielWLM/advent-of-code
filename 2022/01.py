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

    id = 0
    dict = {}
    for line in args.input:
        if line.strip("\n") == "":
            id += 1
            continue
        amount = int(line)
        if id in dict:
            dict[id] += amount
        else:
            dict[id] = amount
    
    top = max(dict.values())
    dict.pop(list(dict.keys())[list(dict.values()).index(top)])
    scd_top = max(dict.values())
    dict.pop(list(dict.keys())[list(dict.values()).index(scd_top)])
    trd_top = max(dict.values())
    top_three = top + scd_top + trd_top

    print("The top elf has {} calories".format(top))
    print("The top three elves have {} calories".format(top_three))

if __name__ == "__main__":
    main()