"""Solution to day 3"""
# import pysnooper


def read_input() -> list[str]:
    """Read the list of numbers on the input file"""
    with open("input.txt", "r", encoding="utf-8") as f:
        return f.readlines()

# Write solution below


def power(inputs: list[str], num1: str, num2: str) -> int:
    return int("".join([num1 if sum(int(input[i]) for input in inputs) > len(inputs)//2 else num2 for i in range(len(inputs[0])-1)]), 2)


# @pysnooper.snoop
def power_two(inputs: list[str], num1: str, num2: str):
    for i in range(len(inputs[0])-1):
        num = num1 if sum(int(input[i])
                          # '1' or '0'
                          for input in inputs) >= len(inputs)//2 else num2
        test = [input for input in inputs if input[i] == num]
        if len(test) == 0:
            continue
        if i > 4:
            print(i, inputs, [input[i] for input in inputs])
        inputs = test
        if i > 4:
            print(i, inputs, [input[i] for input in inputs])
        if len(inputs) == 1:
            return int(inputs[0], 2)


if __name__ == '__main__':
    inputs = read_input()
    print(power(inputs, "1", "0") * power(inputs, "0", "1"))
    print(power_two(inputs, "1", "0") *
          power_two(inputs, "0", "1"))  # 433992 too low 442338
