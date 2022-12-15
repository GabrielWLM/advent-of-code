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
    
    def has_repeats(text):
        length = len(text)
        for i in range(length - 1):
            for j in range(1, length - i):
                if text[i] == text[i+j]:
                    return True
        return False

    char_num = 3
    char_num_2 = char_num
    for line in args.input: 
        marker_found = False
        four = line[:3]
        new_line = line[3:]
        for char in new_line:
            four += char
            char_num += 1
            if not has_repeats(four):
                marker_found = True
                break
            four = four[1:]
        
        # PART TWO
        marker_found_2 = False
        char_num_2 = char_num + 9
        fourteen = four + line[char_num:char_num_2]
        new_line_2 = line[char_num_2:]
        for char in new_line_2:
            fourteen += char
            char_num_2 += 1
            if not has_repeats(fourteen):
                marker_found_2 = True
                break
            fourteen = fourteen[1:]

        if marker_found_2:
            break
        
    print("Num of characters: {}".format(char_num))
    print("Num of characters 2: {}".format(char_num_2))

if __name__ == "__main__":
    main()