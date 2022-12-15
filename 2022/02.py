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

    rps_dict = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
    DRAW = 3
    WIN = 6
    points = 0
    r_points = 0
    for line in args.input:
        round = line.split()
        opp = rps_dict[round[0]]
        player = rps_dict[round[1]]
        if opp == 3 and player == 1:
            points += WIN
        elif opp == 1 and player == 3:
            pass
        elif player > opp:
            points += WIN
        elif player == opp:
            points += DRAW
        points += player

        if player == 2:
            r_points += opp + DRAW
        elif player == 1:
            newp = opp - 1
            if newp == 0:
                newp = 3
            r_points += newp
        elif player == 3:
            newp = opp + 1
            if newp > 3:
                newp = 1
            r_points += newp + WIN

    print("Total score (for wrong interpretation) will be: {}".format(points))
    print("Total real score will be: {}".format(r_points))

if __name__ == "__main__":
    main()