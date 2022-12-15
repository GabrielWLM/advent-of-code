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

    blank_index = 0

    lines = list(args.input)

    for line in lines:
        if line.strip() == "":
            break
        blank_index += 1

    num_cols = lines[blank_index-1]
    num_cols = num_cols.strip()
    num_cols = num_cols.split()
    col_num = len(num_cols)

    counter = blank_index - 2
    stacks = {}
    for i in range(col_num):
        stacks[i+1] = []
    while counter >= 0:
        line = lines[counter]
        for i in range(col_num):
            index = (i*4)+1
            if len(line) <= index:
                break
            char = line[index]
            if char == " ":
                continue
            stacks[i+1].append(char)
        counter -= 1
    
    stacks_two = {key: value[:] for key, value in stacks.items()}

    for i in range(blank_index + 1, len(lines)):
        line_list = lines[i].split()
        moves = int(line_list[1])
        move_from = int(line_list[3])
        move_to = int(line_list[5])

        # PART TWO
        get_blocks = stacks_two[move_from][-moves:]
        stacks_two[move_to].extend(get_blocks)
        stacks_two[move_from] = stacks_two[move_from][:-moves]
        # PART TWO END

        while moves > 0:
            get_block = stacks[move_from].pop()
            stacks[move_to].append(get_block)
            moves -= 1

    top_crates = ""

    for i in range(col_num):
        stack = stacks[i+1]
        if stack:
            top_crates += stack.pop()
    
    top_crates_two = ""

    for i in range(col_num):
        stack = stacks_two[i+1]
        if stack:
            top_crates_two += stack.pop()

    print("Top crates: {}".format(top_crates))
    print("Top crates 9001: {}".format(top_crates_two))

if __name__ == "__main__":
    main()