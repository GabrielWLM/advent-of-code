import argparse
import re
from turtle import pos

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
    y_part_one = 2000000
    sensor_beacon_dict = {}
    impossible_positions = {}

    lines = list(args.input)

    for line in lines:
        stripped = line.strip()
        coordinates = re.findall(r'-?\d+', stripped)

        sx = int(coordinates[0])
        sy = int(coordinates[1])
        bx = int(coordinates[2])
        by = int(coordinates[3])
        sensor_coordinates = (sx, sy)
        beacon_coordinates = (bx, by)
        sensor_beacon_dict[sensor_coordinates] = beacon_coordinates
        
        max_distance = abs(sx - bx) + abs(sy - by)
        if y_part_one in range(sy - max_distance, sy + max_distance + 1):
            for x in range(sx - max_distance, sx + max_distance + 1):
                if (x, y_part_one) == beacon_coordinates:
                    continue
                distance = abs(sx - x) + abs(sy - y_part_one)
                if distance <= max_distance:
                    impossible_positions[(x, y_part_one)] = True
                elif x > sx:
                    break

    imp_pos_part_one = len(impossible_positions.keys())
    print("Total positions that cannot contain beacons in row y=2000000: {}".format(imp_pos_part_one))

    # PART TWO
    beacon_found = False

    # Go through all points right outside range of impossible diamond for each sensor
    for sensor_coordinates, beacon_coordinates in sensor_beacon_dict.items():
        sx = sensor_coordinates[0]
        sy = sensor_coordinates[1]
        bx = beacon_coordinates[0]
        by = beacon_coordinates[1]
        max_distance = abs(sx - bx) + abs(sy - by)
        dx = 0
        for dy in range(-max_distance - 1, max_distance + 1):
            new_y = sy + dy
            new_x1 = sx - dx
            new_x2 = sx + dx
            x_list = [new_x1, new_x2]
            for new_x in x_list:
                if 0 <= new_x <= 4000000 and 0 <= new_y <= 4000000:
                    beacon_found = True
                    for sensor_coordinates, beacon_coordinates in sensor_beacon_dict.items():
                        max_distance = abs(sensor_coordinates[0] - beacon_coordinates[0]) + abs(sensor_coordinates[1] - beacon_coordinates[1])
                        distance = abs(sensor_coordinates[0] - new_x) + abs(sensor_coordinates[1] - new_y)
                        if distance <= max_distance:
                            beacon_found = False
                            break
                    if beacon_found:
                        tuning_frequency = new_x * 4000000 + new_y
                        print(f"Distress beacon location: ({new_x}, {new_y})")
                        print("Beacon tuning frequency: {}".format(tuning_frequency))
                        break
                if beacon_found:
                    break
            if dy < 0:
                dx += 1
            else:
                dx -= 1
            if beacon_found:
                break
        if beacon_found:
            break
    
if __name__ == "__main__":
    main()