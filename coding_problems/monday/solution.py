def light_bulbs(lights, n):
    for round in range(n):
        change = lights[-1] == 1
        for num, i in enumerate(lights):
            if change:
                if i == 1:
                    lights[num] = 0
                else:
                    lights[num] = 1
            else:
                lights[num] = i
            change = i == 1

    return lights
