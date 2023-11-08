import random


def run1():
    print('AAA')
    print('BBB')
    print('CCC')
    print('DDD')

state = 'BEGIN'

def run_begin():
    global state
    print('Начало хода игрока')
    state = 'CHECK_AVAILABLE'

def run_check():
    global state
    print('Есть ли карты играть?')
    if random.randint(1, 10) < 5:
        state = 'PLAY'
    else:
        state = 'DRAW'

def run_play():
    global state
    print('Играем карту!')
    state = 'NEXT_PLAYER'

def run_draw():
    global state
    print('Берем карту :(')
    state = 'CHECK_AVAILABLE_AGAIN'

def run_check_again():
    global state
    print('Берем карту :(')
    state = 'CHECK_AVAILABLE_AGAIN'
    if random.randint(1, 10) < 5:
        state = 'PLAY'
    else:
        state = 'NEXT_PLAYER'



states = {
    'BEGIN': run_begin,
    'CHECK_AVAILABLE': run_check,
    'PLAY': run_play,
    'DRAW': run_draw,
    'CHECK_AVAILABLE_AGAIN': run_check_again
}

def run2():
    while True:
        # model update
        states[state]()
        if state == 'NEXT_PLAYER':
            break
        print('draw')


if __name__ == '__main__':
    run2()
