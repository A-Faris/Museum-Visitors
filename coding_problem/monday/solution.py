"""Solution to day 1"""


def read_input() -> list[str]:
    """Read the list of numbers on the input file"""
    with open("input.txt", "r", encoding="utf-8") as f:
        return f.readlines()


def higher_measurement(depths: list[str], num: int) -> int:
    """Counts if the current measurement is higher than a previous measurement"""
    return sum(1 for i in range(num, len(depths)) if int(depths[i-num]) < int(depths[i]))


if __name__ == '__main__':
    inputs = read_input()
    print(higher_measurement(inputs, 1))
    print(higher_measurement(inputs, 3))
