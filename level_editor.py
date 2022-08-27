import pygame
pygame.init()

# set up pygame game
WIDTH = 1800
HEIGHT = 900
TILE_SIZE = 100
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Space Platformer')
fps = 60
timer = pygame.time.Clock()
# font = pygame.font.Font('freesansbold.ttf', 20)
active_level = 0
active_phase = 3
level = [[0 for _ in range(18)] for _ in range(9)]
level.append([2 for _ in range(18)])
level.append([1 for _ in range(18)])
# load images
bg = pygame.image.load('assets/images/space bg.png')
rock = pygame.transform.scale(pygame.image.load('assets/images/tiles/rock.png'), (100, 100))
ground = pygame.transform.scale(pygame.image.load('assets/images/tiles/ground.png'), (100, 100))
platform = pygame.transform.scale(pygame.image.load('assets/images/tiles/platform.png'), (100, 50))
acid = pygame.transform.scale(pygame.image.load('assets/images/tiles/acid2.png'), (100, 25))
blue_key = pygame.transform.scale(pygame.image.load('assets/images/keycards/key_blue.png'), (60, 100))
green_key = pygame.transform.scale(pygame.image.load('assets/images/keycards/key_green.png'), (60, 100))
red_key = pygame.transform.scale(pygame.image.load('assets/images/keycards/key_red.png'), (60, 100))
yellow_key = pygame.transform.scale(pygame.image.load('assets/images/keycards/key_yellow.png'), (60, 100))
blue_door = pygame.transform.scale(pygame.image.load('assets/images/portals/blue.png'), (100, 100))
green_door = pygame.transform.scale(pygame.image.load('assets/images/portals/green.png'), (100, 100))
red_door = pygame.transform.scale(pygame.image.load('assets/images/portals/red.png'), (100, 100))
yellow_door = pygame.transform.scale(pygame.image.load('assets/images/portals/yellow.png'), (100, 100))
lock = pygame.transform.scale(pygame.image.load('assets/images/lock.png'), (60, 60))
tiles = ['', rock, ground, platform, acid, '']
keys = [blue_key, green_key, red_key, yellow_key]
doors = [blue_door, green_door, red_door, yellow_door]
frames = []
player_scale = 14
for _ in range(1, 5):
    frames.append(pygame.transform.scale(pygame.image.load(f'assets/images/astronaut/{_}.png'),
                                         (5 * player_scale, 8 * player_scale)))


# draw inventory
def draw_inventory():
    font = pygame.font.Font('freesansbold.ttf', 20)
    colors = ['blue', 'green', 'red', 'yellow']
    pygame.draw.rect(screen, 'black', [5, HEIGHT - 120, WIDTH - 10, 110], 0, 5)
    pygame.draw.rect(screen, 'purple', [5, HEIGHT - 120, WIDTH - 10, 110], 3, 5)
    pygame.draw.rect(screen, 'white', [8, HEIGHT - 117, 340, 104], 3, 5)
    pygame.draw.rect(screen, 'white', [348, HEIGHT - 117, 532, 104], 3, 5)
    pygame.draw.rect(screen, 'white', [880, HEIGHT - 117, 910, 104], 3, 5)
    font.italic = True
    inst_text = font.render('Left/Right Click On Spaces', True, 'white')
    inst_text2 = font.render('Or Scroll Wheel', True, 'white')
    inst_text3 = font.render('Press Enter to Print to Console', True, 'white')
    inst_text4 = font.render('Then Copy to Levels.py', True, 'white')
    screen.blit(inst_text, (14, HEIGHT - 113))
    screen.blit(inst_text2, (14, HEIGHT - 88))
    screen.blit(inst_text3, (14, HEIGHT - 63))
    screen.blit(inst_text4, (14, HEIGHT - 38))
    font = pygame.font.Font('freesansbold.ttf', 32)
    level_text = font.render(f'Level: {active_level + 1}', True, 'white')
    screen.blit(level_text, (354, HEIGHT - 110))
    phase_strings = ['Blue', 'Green', 'Red', 'Gold']
    phase_text = font.render(f'Phase: {phase_strings[active_phase]}', True, colors[active_phase])
    screen.blit(phase_text, (354, HEIGHT - 50))
    plus_lvl = pygame.draw.rect(screen, 'gray', [600, HEIGHT - 110, 40, 40], 0, 5)
    minus_lvl = pygame.draw.rect(screen, 'gray', [660, HEIGHT - 110, 40, 40], 0, 5)
    plus_phase = pygame.draw.rect(screen, 'gray', [600, HEIGHT - 60, 40, 40], 0, 5)
    minus_phase = pygame.draw.rect(screen, 'gray', [660, HEIGHT - 60, 40, 40], 0, 5)
    plus_text = font.render('+', True, 'black')
    screen.blit(plus_text, (613, HEIGHT - 107))
    screen.blit(plus_text, (613, HEIGHT - 57))
    minus_text = font.render('-', True, 'black')
    screen.blit(minus_text, (675, HEIGHT - 107))
    screen.blit(minus_text, (675, HEIGHT - 57))

    font = pygame.font.Font('freesansbold.ttf', 44)
    enter_text = font.render('Use the mouse to design the levels', True, 'white')
    screen.blit(enter_text, (900, HEIGHT - 90))

    return [plus_lvl, minus_lvl, plus_phase, minus_phase]


# draw board
def draw_board(board):
    # below ground - 1, walkable ground - 2, platform - 3, acid - 4, 5 - spawn  point, 6-9 keys, 10-13 portals
    for q in range(len(board)):
        for j in range(len(board[q])):
            if board[q][j] != 0:
                value = board[q][j]
                if 0 < value < 4:
                    screen.blit(tiles[value], (j * TILE_SIZE, q * TILE_SIZE))
                elif value == 4:
                    screen.blit(tiles[value], (j * TILE_SIZE, q * TILE_SIZE + 75))
                elif value == 5:
                    screen.blit(frames[0], (j * TILE_SIZE, q * TILE_SIZE - 10))
                elif 6 <= value < 10:
                    screen.blit(keys[value - 6], (j * TILE_SIZE + 20, q * TILE_SIZE))
                elif 10 <= value:
                    screen.blit(doors[value - 10], (j * TILE_SIZE, q * TILE_SIZE))


# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    screen.blit(bg, (0, 0))

    # draw board tiles
    draw_board(level)
    buttons = draw_inventory()

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                board_string = ''
                for i in range(len(level)):
                    board_string += str(level[i]) + ',\n'
                print(f'Level: {active_level}\nPhase: {active_phase}\nBoard: {board_string}')
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_press = False
            for i in range(len(buttons)):
                if buttons[i].collidepoint(event.pos):
                    button_press = True
                    if i == 0:
                        active_level += 1
                    elif i == 1:
                        if active_level > 0:
                            active_level -= 1
                    elif i == 2:
                        if active_phase < 3:
                            active_phase += 1
                        else:
                            active_phase = 0
                    elif i == 3:
                        if active_phase > 0:
                            active_phase -= 1
                        else:
                            active_phase = 3
            if not button_press:
                coords = pygame.mouse.get_pos()[0] // 100, pygame.mouse.get_pos()[1] // 100
                if event.button == 1 or event.button == 4:
                    if level[coords[1]][coords[0]] < 13:
                        level[coords[1]][coords[0]] += 1
                    else:
                        level[coords[1]][coords[0]] = 0
                if event.button == 3 or event.button == 5:
                    if level[coords[1]][coords[0]] > 0:
                        level[coords[1]][coords[0]] -= 1
                    else:
                        level[coords[1]][coords[0]] = 13

    pygame.display.flip()
pygame.quit()
