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

    # Parse Input
    lines = list(args.input)
    tree_grid = [[] for x in range(len(lines))]
    row = 0
    for line in lines:
        line = line.strip()
        for height in line:
            tree_grid[row].append(int(height))
        row += 1

    num_rows = len(tree_grid)
    num_cols = len(tree_grid[0])

    # Count visible trees
    total_visible = 2 * num_cols + 2 * num_rows - 4

    for row in range(1, num_rows - 1):
        for col in range(1, num_cols - 1):
            visible = False
            curr_height = tree_grid[row][col]
            # Check left
            check_col = col - 1
            while check_col >= 0:
                if tree_grid[row][check_col] >= curr_height:
                    break
                if check_col == 0:
                    total_visible += 1
                    visible = True
                    break
                check_col -= 1

            if visible:
                continue
            
            # Check right
            check_col = col + 1
            while check_col < num_cols:
                if tree_grid[row][check_col] >= curr_height:
                    break
                if check_col == num_cols - 1:
                    total_visible += 1
                    visible = True
                    break
                check_col += 1
            
            if visible:
                continue

            # Check up
            check_row = row - 1
            while check_row >= 0:
                if tree_grid[check_row][col] >= curr_height:
                    break
                if check_row == 0:
                    total_visible += 1
                    visible = True
                    break
                check_row -= 1
            
            if visible:
                continue

            # Check down
            check_row = row + 1
            while check_row < num_rows:
                if tree_grid[check_row][col] >= curr_height:
                    break
                if check_row == num_rows - 1:
                    total_visible += 1
                    visible = True
                    break
                check_row += 1
            
            if visible:
                continue

    print("Total visible trees: {}".format(total_visible))

    # PART TWO: Get highest scenic score
    max_score = 0

    for row in range(1, num_rows - 1):
        for col in range(1, num_cols - 1):
            curr_height = tree_grid[row][col]
            # Check left
            left = 0
            check_col = col - 1
            while check_col >= 0:
                left += 1
                if tree_grid[row][check_col] >= curr_height:
                    break
                check_col -= 1
            
            # Check right
            right = 0
            check_col = col + 1
            while check_col < num_cols:
                right += 1
                if tree_grid[row][check_col] >= curr_height:
                    break
                check_col += 1

            # Check up
            up = 0
            check_row = row - 1
            while check_row >= 0:
                up += 1
                if tree_grid[check_row][col] >= curr_height:
                    break
                check_row -= 1

            # Check down
            down = 0
            check_row = row + 1
            while check_row < num_rows:
                down += 1
                if tree_grid[check_row][col] >= curr_height:
                    break
                check_row += 1
            
            curr_score = left * right * up * down
            max_score = max(max_score, curr_score)

    print("Highest Scenic Score: {}".format(max_score))

if __name__ == "__main__":
    main()