import pygame
from time import sleep
import time

BLACK, RED, WHITE = (0, 0, 0), (255, 0, 0), (255, 255, 255)
DIM, DIMMER = (100, 100, 100), (70, 70, 70)
pad_width, pad_height = 480, 640
fight_width, fight_height = 36, 38
enemy_width, enemy_height = 26, 20
origin_mode = False
music_path = './music/1. zomboss.mp3'
record_path = './record/1. zomboss.txt'
def drawScore(count):
    global gamepad
    global combo, max_combo
    font = pygame.font.SysFont(None, 25)
    text = font.render('Enemy Kills: ' + str(count), True, WHITE)
    gamepad.blit(text, (0, 0))
    if combo>max_combo:
        max_combo = combo
    if combo>=2:
        font = pygame.font.SysFont(None, 25)
        text = font.render(str(combo)+' Combo!', True, WHITE)
        gamepad.blit(text, (pad_width/2-30, 0))

def drawLife(count):
    global gamepad
    font = pygame.font.SysFont(None, 25)
    text = font.render('Life: ' + str(count), True, RED)
    gamepad.blit(text, (360, 0))

def dispMessage(text, font = 80, x = pad_width/2, y = pad_height/2, c = RED, update = True, style = 'freesansbold.ttf'):
    global gamepad
    textfont = pygame.font.Font(style, font)
    text = textfont.render(text, True, c)
    textpos = text.get_rect()
    textpos.center = (x, y)
    gamepad.blit(text, textpos)
    if update == True:
        pygame.display.update()

def cleaning():
    global gamepad, origin_mode
    global sector, pos_mode

    gamepad.fill(BLACK)

    if origin_mode == False:
        for k in range(0, sector + 1):
            start_point = [pad_width * k / sector, 0]
            end_point = [pad_width * k / sector, pad_height]
            pygame.draw.line(gamepad, DIM, start_point, end_point, 1)
        pygame.draw.line(gamepad, DIMMER, [0, 555], [pad_width, 555])
        pygame.draw.line(gamepad, DIMMER, [0, 520], [pad_width, 520])
        pygame.draw.line(gamepad, DIMMER, [0, 110], [pad_width, 110])
        pygame.draw.line(gamepad, DIMMER, [0, 100], [pad_width, 100])
        pygame.draw.line(gamepad, DIMMER, [0, 310], [pad_width, 310])
        pygame.draw.line(gamepad, DIMMER, [0, 320], [pad_width, 320])

        key = ['S', 'D', 'F', 'J', 'K', 'L']
        for i in range(sector):
            textfont = pygame.font.Font('freesansbold.ttf', 19)
            text = textfont.render(key[i], True, WHITE)
            textpos = text.get_rect()
            textpos.center = (pos_mode[i] + 14, pad_height - 100)
            gamepad.blit(text, textpos)

def drawObject(obj, x, y, a = None):
    global gamepad
    if a == None:
        gamepad.blit(obj, (x, y))
    else:
        obj2 = obj.copy().convert()
        obj2.set_alpha(a*15)
        gamepad.blit(obj2, (x, y))

def drawUI(ui):
    ui_dict = {0: ui0, 1: ui1, 2: ui2, 3: ui3, 4: ui4, 5: ui5}
    for i in range(len(ui)):
        if ui[i] != 0:
            drawObject(ui_dict[i], pos_mode[i] - 27, 0, a=ui[i])
    for i in range(len(ui)):
        if ui[i] != 0:
            ui[i] -= 1

def bullet_shot(x, y):
    global bullet_xy, key, error
    global ui, pos_mode, enemy_list
    if len(bullet_xy) < 4:
        bullet_x = x + fight_width / 2 - 5
        bullet_y = y - fight_height + 20
        bullet_xy.append([bullet_x, bullet_y])
        if origin_mode == False:
            ui[pos_mode.index(x)] = 15
    else: pygame.mixer.Sound.play(error)
def enemy_generate():
    global key, timer, t1
    global enemy_list, ui
    global shotcount, life
    global pos_mode, origin_mode
    global x, y, bullet_xy

    t2 = time.perf_counter()
    if origin_mode == False and timer[0]-0.2 < t2-t1:
        if int(key[0]) != 6:
            enemy_list.append([pos_mode[int(key[0])], 0])
            del key[0], timer[0]
        else:
            del key[0], timer[0]
            origin_mode = not origin_mode
            ui = [0, 0, 0, 0, 0, 0]
            enemy_list.clear()
            bullet_xy.clear()

    elif origin_mode == True and timer[0]-0.05 < t2-t1:
        if float(key[0]) != 6.0:
            enemy_list.append([float(key[0]), 0])
            del key[0], timer[0]
        else:
            del key[0], timer[0]
            origin_mode = not origin_mode
            x = pos_mode[1]
            y = pad_height * 0.9
            enemy_list.clear()
            bullet_xy.clear()

def select_music():
    from glob import glob
    global gamepad, music_path, clock, record_path
    music_list = sorted(glob('./music/*.mp3'))
    ongame = False
    cursor = 0
    check = pygame.image.load('./image/check.png')
    gamepad.fill(BLACK)

    while not ongame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongame = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cursor -= 1
                    if cursor < 0:
                        cursor = 0
                elif event.key == pygame.K_DOWN:
                    cursor += 1
                    if cursor > len(music_list)-1:
                        cursor = len(music_list)-1
                elif event.key == pygame.K_RETURN:
                    gamepad.fill(BLACK)
                    music_path = music_list[cursor]
                    record_path = './record/'+music_path.split('\\')[-1][:-4]+'.txt'
                    return

                elif event.key == pygame.K_BACKSPACE:
                    gamepad.fill(BLACK)
                    return

        gamepad.fill(BLACK)

        for i in range(len(music_list)):
            dispMessage(music_list[i].split('\\')[-1]+'      ', 20, y=pad_height*(1+i)/(20) , c=WHITE, update = False, style = 'Noto-Black.otf')
        drawObject(check, x=pad_width*3/4, y = pad_height*(cursor+1)/20 - 7)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def mainMenu():
    global origin_mode
    ongame = False
    from level_maker import initMaker, runMaker
    pygame.mixer_music.load('./main_theme.mp3')
    pygame.mixer_music.play(-1)
    while not ongame:
        global gamepad
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongame = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    pygame.mixer_music.stop()
                    origin_mode = False
                    runGame()
                    pygame.mixer_music.load('./main_theme.mp3')
                    pygame.mixer_music.play(-1)

                elif event.key == pygame.K_1:
                    pygame.mixer_music.stop()
                    initMaker(music_path)
                    runMaker(record_path)
                    pygame.mixer_music.load('./main_theme.mp3')
                    pygame.mixer_music.play(-1)

                elif event.key == pygame.K_2:
                    select_music()

                elif event.key == pygame.K_3:
                    ongame = True

        dispMessage('Rhylaga', 60, y = pad_height/4)
        dispMessage('start game: press 0', 25, y = 280, c = DIM)
        dispMessage('make level: press 1', 25, y = 340, c = DIM)
        dispMessage('select music: press 2', 25, y = 400, c = DIM)
        dispMessage('quit: press 3', 25, y = 460, c = DIM)

    pygame.quit()

def runGame():
    global gamepad, fighter, clock
    global bullet, enemy, pos_mode, sector
    global bullet_xy, mistake, t1, origin_mode
    global ui, ui0, ui1, ui2, ui3, ui4, ui5
    global enemy_list, error, shotcount, life
    global x, y, key, timer, record_path
    global combo, max_combo

    pygame.mixer.music.load(music_path)
    pygame.mixer_music.play(0)

    shotcount = 0
    life = 10
    combo = 0
    max_combo = 0

    x = pos_mode[1]
    y = pad_height * 0.9
    x_change, y_change = 0, 0
    t1 = time.perf_counter()

    bullet_xy = []
    enemy_list = []
    ongame = False
    with open(record_path, 'r') as f:
        track = f.readlines()
    track.pop(0)
    key = []
    timer = []
    for cmd in track:
        key.append(cmd.split()[0])
        timer.append(float(cmd.split()[1]))

    while not ongame:
        if len(key) != len(timer):
            raise AssertionError
        elif len(key) == 0:
            gamepad.fill(BLACK)
            pygame.mixer_music.stop()
            while True:
                dispMessage('Good Job!',font = 60 ,y = pad_height/2-100)
                dispMessage('Max_combo = ' + str(max_combo), 25, pad_width/2, pad_height/2+10, WHITE)
                dispMessage('Total_kill = ' + str(shotcount), 25, pad_width/2, pad_height/2+60, WHITE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_BACKSPACE:
                            gamepad.fill(BLACK)
                            pygame.mixer_music.stop()
                            return

        enemy_generate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongame = True

            if origin_mode == False and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    x = pos_mode[0]
                    bullet_shot(x, y)

                elif event.key == pygame.K_d:
                    x = pos_mode[1]
                    bullet_shot(x, y)

                elif event.key == pygame.K_f:
                    x = pos_mode[2]
                    bullet_shot(x, y)

                elif event.key == pygame.K_j:
                    x = pos_mode[3]
                    bullet_shot(x, y)

                elif event.key == pygame.K_k:
                    x = pos_mode[4]
                    bullet_shot(x, y)

                elif event.key == pygame.K_l:
                    x = pos_mode[5]
                    bullet_shot(x, y)

                elif event.key == pygame.K_BACKSPACE:
                    gamepad.fill(BLACK)
                    pygame.mixer_music.stop()
                    return

            elif origin_mode == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change -= 7

                    elif event.key == pygame.K_RIGHT:
                        x_change += 7

                    elif event.key == pygame.K_UP:
                        y_change -= 7

                    elif event.key == pygame.K_DOWN:
                        y_change += 7

                    elif event.key == pygame.K_SPACE:
                        if len(bullet_xy) < 6:
                            bullet_x = x + fight_width/2
                            bullet_y = y - fight_height
                            bullet_xy.append([bullet_x, bullet_y])

                elif event.key == pygame.K_BACKSPACE:
                    gamepad.fill(BLACK)
                    return


                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        y_change = 0

        cleaning()
        if origin_mode == True:
            x += x_change
            y += y_change

        if x < 0:
            x = 0
        elif x > pad_width - fight_width:
            x = pad_width - fight_width
        if y < 0:
            y = 0
        elif y > pad_height - fight_height:
            y = pad_height - fight_height

        # 게이머 전투기가 적과 충돌했는지 체크
        for i in range(len(enemy_list)):
            enemy_x = enemy_list[i][0]
            enemy_y = enemy_list[i][1]
            if y < enemy_y + enemy_height:
                if (enemy_x > x and enemy_x < x + fight_width) or \
                        (enemy_x + enemy_width > x and enemy_x + enemy_width < x + fight_width):
                    enemy_list[i][1] = 9999
                    pygame.mixer.Sound.play(error)
                    combo = 0

        drawObject(fighter, x, y)

        # 전투기 무기 발사 구현
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[1] -= 10
                bullet_xy[i][1] = bxy[1]

                for i in range(len(enemy_list)):
                    enemy_x = enemy_list[i][0]
                    enemy_y = enemy_list[i][1]
                    if bxy[1] < enemy_y:
                        if bxy[0] > enemy_x-5 and bxy[0] < enemy_x + enemy_width+5:
                            bullet_xy.remove(bxy)
                            if i==0 or origin_mode == True:
                                del enemy_list[i]
                                shotcount += 1
                                combo += 1
                            elif abs(enemy_list[0][1] - enemy_list[i][1]) < 20:
                                del enemy_list[i]
                                shotcount += 1
                                combo += 1
                            else:
                                pygame.mixer.Sound.play(error)
                                combo = 0
                            break

                if bxy[1] <= 0:
                    try:
                        bullet_xy.remove(bxy)
                        combo = 0
                    except:
                        pass

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        # 적의 속도, 적을 놓친경우
        del_list = []
        if origin_mode == False:
            enemy_speed = 8
        else:
            enemy_speed = 4

        for i in range(len(enemy_list)):
            enemy_list[i][1] += enemy_speed
            enemy_x = enemy_list[i][0]
            enemy_y = enemy_list[i][1]

            if origin_mode == False:
                limit = 520
            else: limit = pad_height

            if enemy_y > limit:
                del_list.append(i)
                if origin_mode == False:
                    drawObject(mistake, enemy_x - 18, pad_height - 80)
                    combo = 0
                pygame.mixer.Sound.play(error)
                life -= 1

        for index in sorted(del_list, reverse = True):
            del enemy_list[index]

        drawLife(life)
        drawScore(shotcount)
        drawUI(ui)

        for i in range(len(enemy_list)):
            drawObject(enemy, enemy_list[i][0], enemy_list[i][1])

        if life == -1:
            dispMessage('Game Over')
            sleep(2)
            gamepad.fill(BLACK)
            pygame.mixer_music.stop()
            return

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def initGame():
    global gamepad, fighter, clock
    global bullet, enemy
    global sector, ui, mistake
    global pos_mode, key, timer
    global ui0, ui1, ui2, ui3, ui4, ui5
    global error, combo
    combo = 0
    sector = 6
    pos_mode = [pad_width / (sector * 2) - enemy_width / 2]
    for _ in range(sector - 1):
        pos_mode.append(pos_mode[-1] + pad_width / sector)
    ui = [0, 0, 0, 0, 0, 0]

    pygame.init()
    error = pygame.mixer.Sound('./sound/button.wav')
    error.set_volume(0.2)

    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('Rhylaga')
    fighter = pygame.image.load('./image/fighter.png')
    enemy = pygame.image.load('./image/enemy.png')
    bullet = pygame.image.load('./image/bullet.png')

    ui0 = pygame.image.load('./image/ui0.png')
    ui1 = pygame.image.load('./image/ui1.png')
    ui2 = pygame.image.load('./image/ui2.png')
    ui3 = pygame.image.load('./image/ui3.png')
    ui4 = pygame.image.load('./image/ui4.png')
    ui5 = pygame.image.load('./image/ui5.png')
    mistake = pygame.image.load('./image/mistake.png')
    clock = pygame.time.Clock()

initGame()
mainMenu()
