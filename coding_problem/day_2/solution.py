"""Solution to day 2"""


def read_input() -> list[str]:
    """Read the list of numbers on the input file"""
    with open("input.txt", "r", encoding="utf-8") as f:
        return f.readlines()

# Write solution below


def location(inputs: list[str]) -> int:
    """Finds the location of the submarine"""
    horizontal = 0
    depth = 0
    for input_ in inputs:
        direction = input_.split()[0]
        number = int(input_.split()[1])
        match direction:
            case "forward":
                horizontal += number
            case "down":
                depth += number
            case "up":
                depth -= number
    return horizontal * depth


def location_two(inputs: list[str]) -> int:
    """Finds the location of the submarine"""
    horizontal = 0
    aim = 0
    depth = 0
    for input_ in inputs:
        direction = input_.split()[0]
        number = int(input_.split()[1])
        match direction:
            case "forward":
                horizontal += number
                depth += aim * number
            case "down":
                aim += number
            case "up":
                aim -= number
    return horizontal * depth


if __name__ == '__main__':
    inputs = read_input()
    print(location(inputs))
    print(location_two(inputs))
