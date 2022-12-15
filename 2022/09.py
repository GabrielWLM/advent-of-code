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

    # Parse Input and fill up visited grid using (y, x) grid
    visited_positions = {(0, 0)}
    H_pos = (0, 0)
    T_pos = (0, 0)

    visited_positions_nine = {(0, 0)}
    H9_pos = [(0, 0) for x in range(10)]

    for line in args.input:
        line = line.strip()
        split_l = line.split()
        direction = split_l[0]
        num_steps = int(split_l[1])
        if direction == "L":
            for n in range(num_steps):
                H_pos = (H_pos[0], H_pos[1] - 1)
                if T_pos[1] - H_pos[1] > 1:
                    T_pos = (H_pos[0], H_pos[1] + 1)
                    visited_positions.add((H_pos[0], H_pos[1] + 1))
        elif direction == "R":
            for n in range(num_steps):
                H_pos = (H_pos[0], H_pos[1] + 1)
                if H_pos[1] - T_pos[1] > 1:
                    T_pos = (H_pos[0], H_pos[1] - 1)
                    visited_positions.add((H_pos[0], H_pos[1] - 1))
        elif direction == "U":
            for n in range(num_steps):
                H_pos = (H_pos[0] + 1, H_pos[1])
                if H_pos[0] - T_pos[0] > 1:
                    T_pos = (H_pos[0] - 1, H_pos[1])
                    visited_positions.add((H_pos[0] - 1, H_pos[1]))
        elif direction == "D":
            for n in range(num_steps):
                H_pos = (H_pos[0] - 1, H_pos[1])
                if  T_pos[0] - H_pos[0] > 1:
                    T_pos = (H_pos[0] + 1, H_pos[1])
                    visited_positions.add((H_pos[0] + 1, H_pos[1]))

        # PART TWO
        for n in range(num_steps):
            if direction == "L":
                H9_pos[0] = (H9_pos[0][0], H9_pos[0][1] - 1)
            elif direction == "R":
                H9_pos[0] = (H9_pos[0][0], H9_pos[0][1] + 1)
            elif direction == "U":
                H9_pos[0] = (H9_pos[0][0] + 1, H9_pos[0][1])
            elif direction == "D":
                H9_pos[0] = (H9_pos[0][0] - 1, H9_pos[0][1])

            for i in range(1, len(H9_pos)):
                prev_pos = H9_pos[i - 1]
                if H9_pos[i][1] - prev_pos[1] > 1 and H9_pos[i][0] - prev_pos[0] > 1:
                    # Prev now diagonally 2 steps left and down from curr
                    H9_pos[i] = (prev_pos[0] + 1, prev_pos[1] + 1)
                elif H9_pos[i][1] - prev_pos[1] > 1 and prev_pos[0] - H9_pos[i][0] > 1:
                    # Prev now diagonally 2 steps left and up from curr
                    H9_pos[i] = (prev_pos[0] - 1, prev_pos[1] + 1)
                elif prev_pos[1] - H9_pos[i][1] > 1 and H9_pos[i][0] - prev_pos[0] > 1:
                    # Prev now diagonally 2 steps right and down from curr
                    H9_pos[i] = (prev_pos[0] + 1, prev_pos[1] - 1)
                elif prev_pos[1] - H9_pos[i][1] > 1 and prev_pos[0] - H9_pos[i][0] > 1:
                    # Prev now diagonally 2 steps right and up from curr
                    H9_pos[i] = (prev_pos[0] - 1, prev_pos[1] - 1)
                elif H9_pos[i][1] - prev_pos[1] > 1: # Prev now 2 steps left from curr
                    H9_pos[i] = (prev_pos[0], prev_pos[1] + 1)
                elif prev_pos[1] - H9_pos[i][1] > 1: # Prev now 2 steps right from curr
                    H9_pos[i] = (prev_pos[0], prev_pos[1] - 1)
                elif prev_pos[0] - H9_pos[i][0] > 1: # Prev now 2 steps up from curr
                    H9_pos[i] = (prev_pos[0] - 1, prev_pos[1])
                elif H9_pos[i][0] - prev_pos[0] > 1: # Prev now 2 steps down from curr
                    H9_pos[i] = (prev_pos[0] + 1, prev_pos[1])
            
            last_pos = H9_pos[len(H9_pos) - 1]
            visited_positions_nine.add((last_pos[0], last_pos[1]))

    # Count total visited
    total_visited = len(visited_positions)
    total_visited_nine = len(visited_positions_nine)

    print("Total visited positions by T: {}".format(total_visited))
    print("Total visited positions by 9: {}".format(total_visited_nine))

if __name__ == "__main__":
    main()