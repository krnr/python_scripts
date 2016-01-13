import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math

meter = 6
SIDE = 5 * meter
LENGTH = 120 * meter
WIDTH = 70 * meter + SIDE
HEIGHT = WIDTH + SIDE
left_touchline_x = 10 * meter
left_22_x = left_touchline_x + 22 * meter
right_touchline_x = LENGTH - 10 * meter
right_22_x = right_touchline_x - 22 * meter
left_10_x = LENGTH / 2 - 10 * meter
right_10_x = LENGTH / 2 + 10 * meter
left_5_x = left_touchline_x + 5 * meter
right_5_x = right_touchline_x - 5 * meter
dash_start = 2.5
dash_finish = dash_start + 5 
dash_x = []
dash_y = []
radius = 2 * meter
for i in range(0, 70, 10):
    dash_y.append((SIDE + (dash_start + i) * meter, SIDE + (dash_finish + i) * meter))
for i in range(0, 100, 10):
    dash_x.append((left_touchline_x + (dash_start + i) * meter, left_touchline_x + (dash_finish + i) * meter))

ball_coord = [LENGTH / 2, HEIGHT / 2]
HAS_BALL, PLAY_ON = False, False
active_player = 0
players = range(1,23)
grid_start = LENGTH + 5 * meter
grid_step = 25

players_stat = [['Ps+'],['Ps-'],['Rv+'],['Rv-'],['At+'],['At-'],['Lb'],['Mtr'],
                ['MtB'],['Df-'],['Tc+'],['Tc-'],['Rk+'],['Rk-'],['Kk+'],['Kk-'],
                ['Fo+'],['Fo-'],['To']]
players_coord = [[]]
players_travel = [['Total'], ['With the ball']]
players_travel[0].extend([0]*len(players))
players_travel[1].extend([0]*len(players))

PLAYER_IS_DRAGGED = False

for i in range(len(players_stat)):
    players_stat[i].extend([0]*len(players))
for i in players:
    players_coord.append([i * SIDE, WIDTH + SIDE])

def draw_handler(canvas):
    canvas.draw_polygon([(left_touchline_x, SIDE),
                         (right_touchline_x, SIDE),
                         (right_touchline_x, WIDTH),
                         (left_touchline_x, WIDTH)], 2, 'White')
    canvas.draw_polygon([(0, SIDE),
                         (LENGTH, SIDE),
                         (LENGTH, WIDTH),
                         (0, WIDTH)], 4, 'White')
    canvas.draw_line((LENGTH / 2, SIDE), (LENGTH / 2, WIDTH), 2, 'White')
    canvas.draw_line((left_22_x, SIDE), (left_22_x, WIDTH), 2, 'White')
    canvas.draw_line((right_22_x, SIDE), (right_22_x, WIDTH), 2, 'White')
    canvas.draw_text('22', (left_22_x - 15, SIDE + 20), 30, 'White')
    canvas.draw_text('22', (right_22_x - 15, SIDE + 20), 30, 'White')
    for coord in dash_y:
        canvas.draw_line((left_10_x, coord[0]), (left_10_x, coord[1]), 2, 'White')
        canvas.draw_line((right_10_x, coord[0]), (right_10_x, coord[1]), 2, 'White')
        canvas.draw_line((left_5_x, coord[0]), (left_5_x, coord[1]), 2, 'White')
        canvas.draw_line((right_5_x, coord[0]), (right_5_x, coord[1]), 2, 'White')
    for coord in dash_x:
        canvas.draw_line((coord[0], SIDE + 5 * meter), (coord[1], SIDE + 5 * meter), 2, 'White')
        canvas.draw_line((coord[0], SIDE + 15 * meter), (coord[1], SIDE + 15 * meter), 2, 'White')
        canvas.draw_line((coord[0], WIDTH - 5 * meter), (coord[1], WIDTH - 5 * meter), 2, 'White')
        canvas.draw_line((coord[0], WIDTH - 15 * meter), (coord[1], WIDTH - 15 * meter), 2, 'White')
    canvas.draw_circle(ball_coord, 10, 2, 'Red')
    # draw players
    for player in players:
        canvas.draw_text(str(player), (LENGTH + meter, player * SIDE - meter), 20, 'White')
        canvas.draw_circle(players_coord[player], radius, 2, 'Red', 'Red')
        canvas.draw_text(str(player), [players_coord[player][0] - meter, players_coord[player][1] + meter], 14, 'White', 'sans-serif')
        canvas.draw_text(str(players_travel[0][player]), [player * SIDE, WIDTH + SIDE * 3], 14, 'White', 'sans-serif')
        canvas.draw_text(str(players_travel[1][player]), [player * SIDE, WIDTH + SIDE * 4], 14, 'White', 'sans-serif')
    canvas.draw_text('w/o ball', (grid_start - SIDE * 3, WIDTH + SIDE * 3), 14, 'White')
    canvas.draw_text('with ball', (grid_start - SIDE * 3, WIDTH + SIDE * 4), 14, 'White')
    #draw stat grid
    for grid in range(0, 470, grid_step):
        canvas.draw_text(players_stat[grid/grid_step][0], (grid_start + grid, HEIGHT + 198), 14, 'White')
        for player in players:
            canvas.draw_polygon([(grid_start + grid, (player - 1) * SIDE),
                         (grid_start + grid, player * SIDE),
                         (grid_start + grid + grid_step, player * SIDE),
                         (grid_start + grid + grid_step, (player - 1) * SIDE)], 1, 'White')
            if players_stat[grid/grid_step][player] != 0:
                canvas.draw_text(str(players_stat[grid/grid_step][player]), (grid_start + grid + 5, player * SIDE - 5), 20, 'White')    
    
def distance(p, q):
    # used only to define a click on a player - distance from the center of a circle
    return math.sqrt( (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def drag_handler(pos):
    global ball_coord, players_coord, players_travel, PLAYER_IS_DRAGGED
    PLAYER_IS_DRAGGED = True
    for i in players:
        if distance(pos, players_coord[i]) < radius:
            path = math.sqrt(abs(pos[0] - players_coord[i][0])^2*2 + abs(pos[1] - players_coord[i][1])^2)
            # why horizontal path is twice lesser than vertical?
            if PLAYER_IS_DRAGGED:
                players_coord[i][0], players_coord[i][1] = pos[0], pos[1]
                if PLAY_ON and HAS_BALL:
                    players_travel[1][i] += float("%.1f" % (path/meter))
                    players_stat[8][i] += float("%.1f" % (path/meter))
                    # when int(path/meter) it's always 0, only int(path) - makes the pitch 300m long (((
                    # had to use float (((
                elif PLAY_ON:
                    players_travel[0][i] += float("%.1f" % (path/meter))
                    players_stat[7][i] += float("%.1f" % (path/meter))
                    
            PLAYER_IS_DRAGGED = False

def mouse_handler(pos):
    global active_player, players_stat
    if pos[0] > grid_start:
        active_player = pos[1]/SIDE + 1
        action = players_stat[(pos[0] - grid_start) / grid_step][0]
        players_stat[(pos[0] - grid_start) / grid_step][active_player] += 1
        player_label.set_text('Player #' + str(active_player) + " made " + action)

def has_ball_button():
    global HAS_BALL
    if HAS_BALL:
        HAS_BALL = False
    else:
        HAS_BALL = True
    ball_label.set_text('Has the ball: ' + str(HAS_BALL))

def play_on_button():
    global PLAY_ON
    if PLAY_ON:
        PLAY_ON = False
        play_label.set_text('Prepare set')
    else:
        PLAY_ON = True
        play_label.set_text('Play is on')

def recieve():
    global players_coord
    players_coord = [[], [440, 260], [448, 320], [440, 380],
                     [472, 392], [477, 357],
                     [515, 380], [500, 270], [520, 325],
                     [545, 260], [520, 210],
                     [550, 400], [490, 170], [480, 100], [550, 80], [595, 288],
                     [300, WIDTH + SIDE], [330, WIDTH + SIDE], [360, WIDTH + SIDE], [390, WIDTH + SIDE],
                     [420, WIDTH + SIDE], [450, WIDTH + SIDE], [480, WIDTH + SIDE]]

def our_kick():
    global players_coord
    players_coord = [[], [397, 283], [375, 325], [410, 380],
                     [380, 346], [375, 302],
                     [376, 396], [376, 367], [373, 271],
                     [380, 220], [364, 240],
                     [375, 426], [400, 165], [406, 115], [420, 70], [470, 140],
                     [300, WIDTH + SIDE], [330, WIDTH + SIDE], [360, WIDTH + SIDE], [390, WIDTH + SIDE],
                     [420, WIDTH + SIDE], [450, WIDTH + SIDE], [480, WIDTH + SIDE]]

def reset():
    global HAS_BALL, PLAY_ON, active_player, players_stat, players_travel, ball_coord, players_coord
    ball_coord = [LENGTH / 2, HEIGHT / 2]
    HAS_BALL, PLAY_ON = False, False
    active_player = 0
    player_label.set_text('Player #' + str(active_player))
    ball_label.set_text('Has the ball: ' + str(HAS_BALL))
    play_label.set_text('Prepare set')
    players_stat = [['Ps+'],['Ps-'],['Rv+'],['Rv-'],['At+'],['At-'],['Lb'],['Mtr'],
                    ['MtB'],['Df-'],['Tc+'],['Tc-'],['Rk+'],['Rk-'],['Kk+'],['Kk-'],
                    ['Fo+'],['Fo-'],['To']]
    for i in range(len(players_stat)):
        players_stat[i].extend([0]*len(players))
    players_coord = [[]]
    for i in players:
        players_coord.append([i * SIDE, WIDTH + SIDE])
    players_travel = [['Total'], ['With the ball']]
    players_travel[0].extend([0]*len(players))
    players_travel[1].extend([0]*len(players))

frame = simplegui.create_frame('Testing', LENGTH + 500, HEIGHT + 200, 200)
frame.set_canvas_background('green')
frame.set_draw_handler(draw_handler)
frame.set_mousedrag_handler(drag_handler)
frame.set_mouseclick_handler(mouse_handler)
ball_button = frame.add_button('Has the ball', has_ball_button)
play_on_button = frame.add_button('Play on!', play_on_button)
reset_button = frame.add_button('Reset', reset)
recieve_button = frame.add_button('Recieve', recieve)
kick_button = frame.add_button('Our kick', our_kick)
play_label = frame.add_label('Prepare set')
ball_label = frame.add_label('Has the ball: ' + str(HAS_BALL))
player_label = frame.add_label('Player #0')
frame.start()
