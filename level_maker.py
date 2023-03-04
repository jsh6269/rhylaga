import pygame
import time

BLACK, RED, WHITE = (0, 0, 0), (255, 0, 0), (255, 255, 255)
DIM, DIMMER = (100, 100, 100), (70, 70, 70)
pad_width, pad_height = 480, 640
fight_width, fight_height = 36, 38
enemy_width, enemy_height = 26, 20
mode = True

def cleaning():
    global gamepad
    global sector, pos_mode

    gamepad.fill(BLACK)
    if mode == True:
        for k in range(0, sector + 1):
            start_point = [pad_width * k / sector, 0]
            end_point = [pad_width * k / sector, pad_height]
            pygame.draw.line(gamepad, DIM, start_point, end_point, 1)
        pygame.draw.line(gamepad, DIMMER, [0, 555], [pad_width, 555])
        pygame.draw.line(gamepad, DIMMER, [0, 520], [pad_width, 520])

        key = ['S', 'D', 'F', 'J', 'K', 'L']
        for i in range(sector):
            textfont = pygame.font.Font('freesansbold.ttf', 19)
            text = textfont.render(key[i], True, WHITE)
            textpos = text.get_rect()
            textpos.center = (pos_mode[i] + 14, pad_height - 100)
            gamepad.blit(text, textpos)

def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))

def bullet_shot(x, y):
    global bullet_xy
    bullet_x = x + fight_width / 2 - 5
    bullet_y = y - fight_height + 20
    bullet_xy.append([bullet_x, bullet_y])

def record(key, record_path):
    global t1
    t2 = time.perf_counter()
    with open(record_path, 'a') as f:
        f.write(key)
        f.write(' ')
        f.write(str(t2-t1))
        f.write('\n')

def runMaker(record_path):
    global gamepad, fighter, clock
    global bullet, pos_mode, sector
    global bullet_xy
    global t1, mode

    t1 = time.perf_counter()
    x = pos_mode[1]
    y = pad_height * 0.9
    x_change = 0
    y_change = 0
    bullet_xy = []
    ongame = False
    mode = True

    with open(record_path , 'w') as f:
        f.write('Header')
        f.write('\n')

    while not ongame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongame = True

            if event.type == pygame.KEYDOWN:
                if mode == True:
                    if event.key == pygame.K_s:
                        x = pos_mode[0]
                        bullet_shot(x, y)
                        record('0', record_path)

                    elif event.key == pygame.K_d:
                        x = pos_mode[1]
                        bullet_shot(x, y)
                        record('1', record_path)

                    elif event.key == pygame.K_f:
                        x = pos_mode[2]
                        bullet_shot(x, y)
                        record('2', record_path)

                    elif event.key == pygame.K_j:
                        x = pos_mode[3]
                        bullet_shot(x, y)
                        record('3', record_path)

                    elif event.key == pygame.K_k:
                        x = pos_mode[4]
                        bullet_shot(x, y)
                        record('4', record_path)

                    elif event.key == pygame.K_l:
                        x = pos_mode[5]
                        bullet_shot(x, y)
                        record('5', record_path)

                    elif event.key == pygame.K_LCTRL:
                        record('6', record_path)
                        mode = not mode

                    elif event.key == pygame.K_RETURN:
                        gamepad.fill(BLACK)
                        pygame.mixer_music.stop()
                        return
                else:
                    if event.key == pygame.K_LEFT:
                        x_change -= 7
                    elif event.key == pygame.K_RIGHT:
                        x_change += 7
                    elif event.key == pygame.K_UP:
                        y_change -= 7
                    elif event.key == pygame.K_DOWN:
                        y_change += 7
                    elif event.key == pygame.K_SPACE:
                        bullet_shot(x, y)
                        record(str(x), record_path)
                    elif event.key == pygame.K_LCTRL:
                        mode = not mode
                        y = pad_height * 0.9
                        x = pos_mode[1]
                        record('6', record_path)
                    elif event.key == pygame.K_RETURN:
                        gamepad.fill(BLACK)
                        pygame.mixer_music.stop()
                        return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        if mode == False:
            x += x_change
            y += y_change
        cleaning()

        if x < 0:
            x = 0
        elif x > pad_width - fight_width:
            x = pad_width - fight_width

        if y < 0:
            y = 0
        elif y > pad_height - fight_height:
            y = pad_height - fight_height

        drawObject(fighter, x, y)
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[1] -= 10
                bullet_xy[i][1] = bxy[1]

                if bxy[1] <= 0:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def initMaker(music_path):
    global gamepad, fighter, clock
    global bullet
    global sector
    global pos_mode

    sector = 6
    pos_mode = [pad_width / (sector * 2) - enemy_width / 2]
    for _ in range(sector - 1):
        pos_mode.append(pos_mode[-1] + pad_width / sector)

    pygame.init()
    pygame.mixer.music.load(music_path)
    pygame.mixer_music.play(0)

    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('Rhylaga')
    fighter = pygame.image.load('./image/fighter.png')
    bullet = pygame.image.load('./image/bullet.png')
    clock = pygame.time.Clock()

if __name__ == '__main__':
    initMaker()
    runMaker()