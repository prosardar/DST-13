import numpy as np

def game_core_v1(number, highValue):
    count = 0
    while True:
        count += 1
        predict = np.random.randint(1, highValue)
        if number == predict:
            return(count)

def game_core_v2(number, highValue):
    count = 0
    predict = highValue
    maxValue = highValue
    minValue = 0
    while number != predict:
        count += 1
        if number > predict:
            minValue = predict
            centr = (maxValue - minValue) // 2
            if centr > 0:
                predict += centr
            else:
                predict += 1
        elif number < predict:
            maxValue = predict
            centr = (maxValue - minValue) // 2
            if centr > 0:
                predict -= centr
            else:
                predict -= 1
    return(count)

def score_game(core):
    highValue = 101
    count_ls = []
    np.random.seed(1)
    random_array = np.random.randint(1, highValue, size=(1000))
    for number in random_array:
        count_ls.append(core(number, highValue))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)

# запускаем
score_game(game_core_v2)