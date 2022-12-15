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

    total_SSS = 0
    X = 1
    cycle = 1
    interesting_cycles = [20 + 40 * i for i in range(6)]
    i_cycle_index = 0

    def drawPixel(cycle, X):
        CRT_pos = (cycle - 1) % 40
        if CRT_pos == 0:
            print('')
        if CRT_pos in range(X-1, X+2):
            print('#', end='')
        else:
            print('.', end='')

    drawPixel(cycle, X)

    for line in args.input:
        line = line.strip()
        command = line.split()
        if command[0] == "noop":
            cycle += 1
            drawPixel(cycle, X)
        else:
            cycle += 1
            drawPixel(cycle, X)
            cycle += 1
            if i_cycle_index < len(interesting_cycles) and cycle >= interesting_cycles[i_cycle_index] + 1:
                total_SSS += interesting_cycles[i_cycle_index] * X
                i_cycle_index += 1
            X += int(command[1])
            drawPixel(cycle, X)
        
    print("Total 6 Signal Strengths: {}".format(total_SSS))

if __name__ == "__main__":
    main()