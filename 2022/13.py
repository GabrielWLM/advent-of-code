import argparse
import json

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
    
    # Parse input
    temp = []
    pairs = []
    line_count = 0

    for line in args.input:
        if line_count % 3 == 0:
            temp = line.strip()
        elif line_count % 3 == 1:
            pairs.append((temp, line.strip()))
        line_count += 1

    # Main algorithm
    def is_in_right_order(left, right):
        # Both left and right are integers
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return 1
            elif left > right:
                return -1
            else:
                 return 0
        # Both left and right are lists
        elif isinstance(left, list) and isinstance(right, list):
            index = 0
            while index < min(len(left), len(right)):
                result = is_in_right_order(left[index], right[index])
                if not result == 0:
                    return result
                else:
                    index += 1
            # All comparable items are the same but one list has fewer items
            if len(left) < len(right):
                return 1
            elif len(left) > len(right):
                return -1
            else:
                return 0
        # Exactly one value is an integer
        else:
            if isinstance(left, int):
                return is_in_right_order([left], right)
            else:
                return is_in_right_order(left, [right])
    sum_of_indices = 0
    index = 1

    for pair in pairs:
        if is_in_right_order(json.loads(pair[0]), json.loads(pair[1])) > 0:
            sum_of_indices += index
        index += 1

    print("Sum of indices of pairs in right order: {}".format(sum_of_indices))

    # PART TWO
    divider_one = '[[2]]'
    divider_two = '[[6]]'

    packet_list = [divider_one, divider_two]
    for pair in pairs:
        # Insert left
        for i in range(len(packet_list)):
            left_vs_packet = is_in_right_order(json.loads(pair[0]), json.loads(packet_list[i]))
            if left_vs_packet > 0:
                packet_list.insert(i, pair[0])
                break
            if i == len(packet_list) - 1:
                packet_list.append(pair[0])
        # Insert right
        for i in range(len(packet_list)):
            right_vs_packet = is_in_right_order(json.loads(pair[1]), json.loads(packet_list[i]))
            if right_vs_packet > 0:
                packet_list.insert(i, pair[1])
                break
            if i == len(packet_list) - 1:
                packet_list.append(pair[1])
    
    index_one = packet_list.index(divider_one) + 1
    index_two = packet_list.index(divider_two) + 1

    decoder_key = index_one * index_two

    print("Decoder key: {}".format(decoder_key))

if __name__ == "__main__":
    main()