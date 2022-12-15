import argparse
from math import inf

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

    lines = list(args.input)
    grid = list(map(lambda line: line.strip(), lines))
    direction_signs = ['<', '>', '^', 'V']
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def possible_moves(curr_pos, travelled_pos, low_to_high):
        pos_moves = []
        curr_height = grid[curr_pos[0]][curr_pos[1]]

        dir_index = 0
        for dir in directions:
            new_pos = (curr_pos[0] + dir[0], curr_pos[1] + dir[1])
            
            if new_pos[0] < 0 or new_pos[0] >= len(grid):
                pass
            elif new_pos[1] < 0 or new_pos[1] >= len(grid[0]):
                pass
            elif new_pos in travelled_pos:
                pass
            else:
                if curr_height == 'S':
                    curr_height = 'a'

                new_height = grid[new_pos[0]][new_pos[1]]
                if new_height == 'E':
                    new_height = 'z'
                
                if low_to_high:
                    if ord(new_height) - ord(curr_height) <= 1:
                        pos_moves.append((new_pos, dir_index))
                else:
                    if ord(curr_height) - ord(new_height) <= 1:
                        pos_moves.append((new_pos, dir_index))
            dir_index += 1

        return pos_moves

    def iterative_BFS(start_pos, target, low_to_high):
        travelled_pos = {}
        step_count = 0
        pos_moves = possible_moves(start_pos, travelled_pos, low_to_high)
        next_moves = []
        travelled_pos[start_pos] = True
        path = []

        for next_move, dir_index in pos_moves:
            travelled_pos[next_move] = True
            new_path = path.copy()
            new_path.append(dir_index)
            next_moves.append((next_move, step_count + 1, new_path))

        while(len(next_moves) > 0):
            curr_pos, step_count, path = next_moves.pop(0)
            curr_height = grid[curr_pos[0]][curr_pos[1]]
            
            if curr_height == target:
                return step_count, path
            
            pos_moves = possible_moves(curr_pos, travelled_pos, low_to_high)

            for next_move, dir_index in pos_moves:
                travelled_pos[next_move] = True
                new_path = path.copy()
                new_path.append(dir_index)
                next_moves.append((next_move, step_count + 1, new_path))

        return inf

    def draw_grid(curr_pos, path):
        drawn_grid = [['.' for col in range(len(grid[0]))] for row in range(len(grid))]
        for dir_index in path:
            drawn_grid[curr_pos[0]][curr_pos[1]] = direction_signs[dir_index]
            dir = directions[dir_index]
            curr_pos = (curr_pos[0] + dir[0], curr_pos[1] + dir[1])
        
        for row in drawn_grid:
            for pos in row:
                print(pos, end='')
            print('')

    S_pos = 0
    E_pos = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'S':
                S_pos = (row, col)
            if grid[row][col] == 'E':
                E_pos = (row, col)
    
    min_steps, path = iterative_BFS(start_pos=S_pos, target='E', low_to_high=True)

    print("Minimum steps from S to E: {}".format(min_steps))
    draw_grid(S_pos, path)

    # PART TWO
    min_steps_from_a, path_two = iterative_BFS(start_pos=E_pos, target='a', low_to_high=False) # Assume not from S
    print("Minimum steps from any a to E: {}".format(min_steps_from_a))
    draw_grid(E_pos, path_two)

if __name__ == "__main__":
    main()