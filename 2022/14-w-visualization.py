import argparse
import functools

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
    lines = args.input
    rocks = {}
    SAND_START = (500, 0)

    for line in lines:
        stripped = line.strip()
        points = [eval('(' + point + ')') for point in stripped.split(' -> ')]

        prev_point = points[0] 
        for i in range(1, len(points)):
            
            curr_point = points[i]
            
            if curr_point[0] == prev_point[0]:
                for y in range(min(prev_point[1], curr_point[1]), max(prev_point[1], curr_point[1]) + 1):
                    rocks[(curr_point[0], y)] = True
            elif curr_point[1] == prev_point[1]:
                for x in range(min(prev_point[0], curr_point[0]), max(prev_point[0], curr_point[0]) + 1):
                    rocks[(x, curr_point[1])] = True
            
            prev_point = curr_point

    rocks_list = list(rocks.keys())
    min_rocks_x_y = functools.reduce(lambda a, b: (min(a[0], b[0]), min(a[1], b[1])), rocks_list)
    max_rocks_x_y = functools.reduce(lambda a, b: (max(a[0], b[0]), max(a[1], b[1])), rocks_list)

    # Main Algorithm
    pos_sand = SAND_START
    sand_in_void = False
    resting_sand = {}

    def is_not_blocked(pos, rocks, sand):
        return pos not in rocks and pos not in sand
    
    while(not sand_in_void):
        # Produce new sand
        pos_sand = SAND_START
        rested = False

        while(not rested and not sand_in_void):
            # Falls down
            if is_not_blocked((pos_sand[0], pos_sand[1] + 1), rocks, resting_sand):
                pos_sand = (pos_sand[0], pos_sand[1] + 1)
            # Falls diagonally down and left
            elif is_not_blocked((pos_sand[0] - 1, pos_sand[1] + 1), rocks, resting_sand):
                pos_sand = (pos_sand[0] - 1, pos_sand[1] + 1)
            # Falls diagonally down and right
            elif is_not_blocked((pos_sand[0] + 1, pos_sand[1] + 1), rocks, resting_sand):
                pos_sand = (pos_sand[0] + 1, pos_sand[1] + 1)
            # Comes to a rest
            else:
                resting_sand[pos_sand] = True
                rested = True
            
            # Checks for sand in void
            if (pos_sand[0] < min_rocks_x_y[0]
            or pos_sand[0] > max_rocks_x_y[0]
            or pos_sand[1] > max_rocks_x_y[1]):
                sand_in_void = True

    resting_sand_count = len(resting_sand)
    print("Total units of resting sand: {}".format(resting_sand_count))

    # VISUALISATION
    def draw_grid(rocks, resting_sand, x_range, y_range):
        for y in range(y_range[0], y_range[1] + 1):
            for x in range(x_range[0], x_range[1] + 1):
                if (x, y) in rocks:
                    print('#', end='')
                elif (x, y) in resting_sand:
                    print('o', end='')
                elif (x, y) == SAND_START:
                    print('+', end='')
                else:
                    print('.', end='')
            print('')
        print('')

    x_range = (min(SAND_START[0], min_rocks_x_y[0]), max(SAND_START[0], max_rocks_x_y[0]))
    y_range = (min(SAND_START[1], min_rocks_x_y[1]), max(SAND_START[1], max_rocks_x_y[1]))
    draw_grid(rocks_list, resting_sand, x_range, y_range)

    # PART TWO
    # Establish floor
    rocks_w_floor = rocks.copy()
    resting_sand_two = resting_sand.copy()

    floor_x_range = [x_range[0] - 2, x_range[1] + 2]
    floor_y = max_rocks_x_y[1] + 2

    for x in range(floor_x_range[0], floor_x_range[1] + 1):
        rocks_w_floor[(x, floor_y)] = True

    # Main Algorithm
    pos_sand = SAND_START
    source_blocked = False
    
    while(not source_blocked):
        # Produce new sand
        pos_sand = SAND_START
        rested = False

        while(not rested and not source_blocked):
            # Falls down
            if is_not_blocked((pos_sand[0], pos_sand[1] + 1), rocks_w_floor, resting_sand_two):
                pos_sand = (pos_sand[0], pos_sand[1] + 1)
            # Falls diagonally down and left
            elif is_not_blocked((pos_sand[0] - 1, pos_sand[1] + 1), rocks_w_floor, resting_sand_two):
                pos_sand = (pos_sand[0] - 1, pos_sand[1] + 1)
                # Extend floor to the left
                if pos_sand[0] <= floor_x_range[0] + 1:
                    floor_x_range[0] -= 1
                    rocks_w_floor[(floor_x_range[0], floor_y)] = True
            # Falls diagonally down and right
            elif is_not_blocked((pos_sand[0] + 1, pos_sand[1] + 1), rocks_w_floor, resting_sand_two):
                pos_sand = (pos_sand[0] + 1, pos_sand[1] + 1)
                # Extend floor to the right
                if pos_sand[0] >= floor_x_range[1] - 1:
                    floor_x_range[1] += 1
                    rocks_w_floor[(floor_x_range[1], floor_y)] = True
            # Comes to a rest
            else:
                resting_sand_two[pos_sand] = True
                rested = True
                # Checks for sand resting at source
                if pos_sand == SAND_START:
                    source_blocked = True

    resting_sand_count_two = len(resting_sand_two)
    print("Total units of resting sand with floor: {}".format(resting_sand_count_two))

    x_range = floor_x_range
    y_range = (y_range[0], floor_y)
    draw_grid(rocks_w_floor, resting_sand_two, x_range, y_range)

if __name__ == "__main__":
    main()