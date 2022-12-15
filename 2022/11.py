import argparse
from math import lcm

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
    monkeys = []
    monkeys_two = []
    monkey_num = 0
    monkeys.append({})
    monkeys_two.append({})

    for row in args.input:
        line = row.strip()

        if len(line) == 0:
            # Add monkey
            monkey_num += 1
            monkeys.append({})
            monkeys_two.append({})
            continue
        elif line[0] == 'M':
            continue
        elif line[0] == 'S':
            splits = line.split()
            items = []
            items_two = []
            for index in range(2, len(splits)):
                item = splits[index].strip(',')
                items.append(int(item))
                items_two.append(int(item))
            monkeys[monkey_num]["items"] = items
            monkeys_two[monkey_num]["items"] = items_two
        elif line[0] == 'O':
            splits = line.split()
            monkeys[monkey_num]["op"] = splits[-2]
            monkeys[monkey_num]["op_num"] = splits[-1]
            monkeys_two[monkey_num]["op"] = splits[-2]
            monkeys_two[monkey_num]["op_num"] = splits[-1]
        elif line[0] == 'T':
            splits = line.split()
            monkeys[monkey_num]["div"] = int(splits[-1])
            monkeys_two[monkey_num]["div"] = int(splits[-1])
        elif line[0] == 'I':
            if line[3] == 't':
                splits = line.split()
                monkeys[monkey_num]["true"] = int(splits[-1])
                monkeys_two[monkey_num]["true"] = int(splits[-1])
            elif line[3] == 'f':
                splits = line.split()
                monkeys[monkey_num]["false"] = int(splits[-1])
                monkeys_two[monkey_num]["false"] = int(splits[-1])
    
    inspected_counts = [0 for x in range(len(monkeys))]

    # Run simulation for 20 rounds
    for round in range(20):
        for monkey_num in range(len(monkeys)):
            while(len(monkeys[monkey_num]["items"]) > 0):
                curr_item = monkeys[monkey_num]["items"].pop(0)
                
                new_item = 0
                op_num = 0
                if monkeys[monkey_num]["op_num"] == 'old':
                    op_num = curr_item
                else:
                    op_num = int(monkeys[monkey_num]["op_num"])

                if monkeys[monkey_num]["op"] == '*':
                    new_item = curr_item * op_num
                elif monkeys[monkey_num]["op"] == '+':
                    new_item = curr_item + op_num
                
                new_item = int(new_item / 3)
                inspected_counts[monkey_num] += 1

                if new_item % monkeys[monkey_num]["div"] == 0:
                    throw_to = monkeys[monkey_num]["true"]
                    monkeys[throw_to]["items"].append(new_item)
                else:
                    throw_to = monkeys[monkey_num]["false"]
                    monkeys[throw_to]["items"].append(new_item)

    most_active = max(inspected_counts)
    inspected_counts.remove(most_active)
    sec_most_active = max(inspected_counts)
    MB_level = most_active * sec_most_active
    
    print("Monkey Business Level: {}".format(MB_level))

    # PART TWO
    inspected_counts = [0 for x in range(len(monkeys_two))]

    lcm_of_divs = 1

    for monkey_num in range(len(monkeys_two)):
        lcm_of_divs = lcm(lcm_of_divs, monkeys_two[monkey_num]["div"])

    # Run simulation for 10000 rounds
    for round in range(10000):
        for monkey_num in range(len(monkeys_two)):
            while(len(monkeys_two[monkey_num]["items"]) > 0):
                curr_item = monkeys_two[monkey_num]["items"].pop(0)

                new_item = 0
                op_num = 0
                if monkeys_two[monkey_num]["op_num"] == 'old':
                    op_num = curr_item
                else:
                    op_num = int(monkeys_two[monkey_num]["op_num"])

                if monkeys_two[monkey_num]["op"] == '*':
                    new_item = curr_item * op_num
                elif monkeys_two[monkey_num]["op"] == '+':
                    new_item = curr_item + op_num
                
                mod_new_item = new_item % lcm_of_divs
                
                inspected_counts[monkey_num] += 1

                if mod_new_item % monkeys_two[monkey_num]["div"] == 0:
                    throw_to = monkeys_two[monkey_num]["true"]
                    monkeys_two[throw_to]["items"].append(mod_new_item)
                else:
                    throw_to = monkeys_two[monkey_num]["false"]
                    monkeys_two[throw_to]["items"].append(mod_new_item)

    most_active = max(inspected_counts)
    inspected_counts.remove(most_active)
    sec_most_active = max(inspected_counts)
    MB_level = most_active * sec_most_active
    
    print("Monkey Business Level TWO: {}".format(MB_level))
    
if __name__ == "__main__":
    main()