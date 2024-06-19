import curses
import random
import HiddenCurser
import time
stdscr = curses.initscr()
maxl:int = curses.LINES - 1
maxc:int = curses.COLS - 1
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
#stdscr.nodelay(True)
HiddenCurser.hide()

world: list = []
cursity = 0.03
pchar = "🐻"
enemy = "🐝"
foods = ["🍯","🍯","🍯","🍯", "🍔", "🥜"]
barrier = "🌲"

"""""pchar = "✈"
enemy = "✖"
foods = ["◼", "☁", "☀"]
barrier = "❄"""

food_number = 15
food = []
score = 0

def init():
    global players_c, players_l
    
    for i in range(maxl):
        world.append([])
        for j in range(maxc):
            char = ' ' if random.random() > cursity else barrier
            world[i].append(char)
    #making the foods
    for i in range(food_number):
        food.append(new_food())
    players_l, players_c = random_place()

def new_food():
    fl, fc = random_place()
    fa = random.randint(0, 1000)
    fchar = foods[random.randint(0, len(foods)-1)]
    return (fl, fc, fchar, fa)

def draw():
    
    #showing the world
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addstr(i, j, world[i][j])
    #showing the score
    stdscr.addstr(0, 0, f"Score = {score}")
    #showing foods
    for f in food:
        fl, fc, fchar, fa = f
        stdscr.addstr(fl, fc, fchar)

    #showing the player
    stdscr.addstr(players_l, players_c, pchar)
    stdscr.refresh()

def move(c):
    global players_c, players_l
    if (c == 'w' or c == curses.KEY_UP) and players_l > 0 and world[players_l-1][players_c] != barrier:
        players_l -= 1
        stdscr.refresh()
    elif (c == 's' or c == curses.KEY_DOWN) and maxl + 1 > players_l and world[players_l+1][players_c] != barrier:
        players_l += 1
        stdscr.refresh()
    elif (c == 'd' or c == curses.KEY_RIGHT) and maxc + 1 > players_c and world[players_l][players_c+1] != barrier:
        players_c += 1
        stdscr.refresh()
    elif (c == 'a' or c == curses.KEY_LEFT) and players_c > 0 and world[players_l][players_c-1] != barrier:
        players_c -= 1
        stdscr.refresh()

    players_l = in_range(players_l, 0, maxl - 1)
    players_c = in_range(players_c, 0, maxc - 1)

def check_food():
    global score
    for i in range(len(food)):
        fl, fc, fchar, fa = food[i]
        if fl == players_l and fc == players_c:
            if fchar == foods[-1]:
                score -= 10
            elif fchar == foods[0]:
                score += 5
            elif fchar == foods[-2]:
                score += 10
            nf = new_food()
            food[i] = nf

def in_range(a, min, max):
    if a > max:
        return max
    if a < min:
        return min
    return a

def random_place():
    a = random.randint(0, maxl)
    b = random.randint(0, maxc) 
    while world[a][b] != ' ':        
        a = random.randint(0, maxl)
        b = random.randint(0, maxc)
    return a, b
init()
playing = True

stdscr.addstr("""
    You are a hungry bear seeking for honey
      each honey gives you one point
      each burger gives you ten points
      but you are alergic to peanuts and they can decrease you points
      and also you should becarful of bees

      PRESS ANY KEY TO START
      """)
while playing and score >= 0 :
    #try:
    c = stdscr.getkey()
    #except:
        #c = ""
    if c in 'asdw' or c in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
        move(c)
    elif c == 'q':
        stdscr.clear()
        stdscr.refresh()
        quit()
    check_food()
    draw()


stdscr.clear()
stdscr.refresh()

stdscr.addstr(int(maxl/2), int(maxc/2), "WASTED")
stdscr.refresh()

time.sleep(2)
stdscr.clear()
stdscr.refresh()