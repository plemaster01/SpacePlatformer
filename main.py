import pygame
import levels
from levels import *

pygame.init()

# set up pygame game
WIDTH = 1800
HEIGHT = 900
TILE_SIZE = 100
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Space Platformer')
fps = 60
timer = pygame.time.Clock()
counting = pygame.time.Clock()
# font = pygame.font.Font('freesansbold.ttf', 20)
active_level = 2
active_phase = 3
level = levels[active_level][active_phase]
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
# load sounds
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/song2.mp3')
pygame.mixer.music.set_volume(.2)
pygame.mixer.music.play(-1)
acid_sound = pygame.mixer.Sound('assets/sounds/acid.mp3')
portal_sound = pygame.mixer.Sound('assets/sounds/fast woosh.mp3')
end_sound = pygame.mixer.Sound('assets/sounds/victory.mp3')
jump_sound = pygame.mixer.Sound('assets/sounds/leap.mp3')
key_sound = pygame.mixer.Sound('assets/sounds/key_acquire.mp3')

# game variables
direction = 1  # 1 = right, -1 = left
for _ in range(len(level)):
    if 5 in level[_]:
        start_pos = (_, level[_].index(5))
player_x = start_pos[1] * 100
player_y = start_pos[0] * 100 - (8 * player_scale - 100)
init_x = player_x
init_y = player_y
counter = 0
mode = 'idle'
player_speed = 10
x_change = 0
y_change = 0
gravity = .5
colliding = 0
lives = 5
in_air = False
jump_height = 14
inventory = [False, False, False, False]  # blue, green, red, yellow
enter_message = False
win = False
lose = False
time = 0
second_count = 0


def teleport(index, active_phaz):
    active = active_phaz
    coords = (0, 0)
    for q in range(len(levels[active_level])):
        for p in range(len(levels[active_level][q])):
            if index + 10 in levels[active_level][q][p] and q != active_phaz:
                y_pos = p
                x_pos = levels[active_level][q][p].index(index + 10)
                coords = (x_pos, y_pos)
                active = q
    return active, coords


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
    inventory_text = font.render('Inventory:', True, 'white')
    screen.blit(inventory_text, (14, HEIGHT - 113))
    for q in range(4):
        pygame.draw.rect(screen, colors[q], [10 + (80 * q), HEIGHT - 88, 70, 70], 5, 5)
        if inventory[q]:
            scaled_key = pygame.transform.scale(keys[q], (40, 70))
            screen.blit(scaled_key, (25 + (80 * q), HEIGHT - 88))
    font = pygame.font.Font('freesansbold.ttf', 32)
    level_text = font.render(f'Level: {active_level + 1}', True, 'white')
    screen.blit(level_text, (354, HEIGHT - 110))
    phase_strings = ['Blue', 'Green', 'Red', 'Gold']
    phase_text = font.render(f'Phase: {phase_strings[active_phase]}', True, colors[active_phase])
    screen.blit(phase_text, (354, HEIGHT - 80))
    lives_text = font.render(f'Lives: {lives}', True, 'green')
    screen.blit(lives_text, (354, HEIGHT - 50))
    time_text = font.render(f'Elapsed Time:', True, 'white')
    time_text2 = font.render(f'{time * 2.5} seconds', True, 'white')
    screen.blit(time_text, (600, HEIGHT - 110))
    screen.blit(time_text2, (600, HEIGHT - 80))

    if enter_message:
        font = pygame.font.Font('freesansbold.ttf', 44)
        enter_text = font.render('Press Enter to Go Through Portal!', True, 'white')
        screen.blit(enter_text, (900, HEIGHT - 90))
    else:
        font = pygame.font.Font('freesansbold.ttf', 44)
        enter_text = font.render('Collect Keys and Get To The Gold Door!!', True, 'white')
        screen.blit(enter_text, (900, HEIGHT - 90))


# draw astronaut
def draw_player(count, direc, mod):
    if mod != 'idle':
        if direc == 1:
            screen.blit(frames[count // 5], (player_x, player_y))
        else:
            screen.blit(pygame.transform.flip(frames[count // 5], True, False), (player_x, player_y))
    else:
        if direc == 1:
            screen.blit(frames[0], (player_x, player_y))
        else:
            screen.blit(pygame.transform.flip(frames[0], True, False), (player_x, player_y))


# draw board
def draw_board(board):
    # below ground - 1, walkable ground - 2, platform - 3, acid - 4, 5 - spawn  point, 6-9 keys, 10-13 portals
    acids = []
    for q in range(len(board)):
        for j in range(len(board[q])):
            if board[q][j] != 0:
                value = board[q][j]
                if 0 < value < 4:
                    screen.blit(tiles[value], (j * TILE_SIZE, q * TILE_SIZE))
                elif value == 4:
                    screen.blit(tiles[value], (j * TILE_SIZE, q * TILE_SIZE + 75))
                    acids.append(pygame.rect.Rect((j * TILE_SIZE, q * TILE_SIZE), (100, 25)))
                elif 6 <= value < 10:
                    if not inventory[value - 6]:
                        screen.blit(keys[value - 6], (j * TILE_SIZE + 20, q * TILE_SIZE))
                elif 10 <= value:
                    screen.blit(doors[value - 10], (j * TILE_SIZE, q * TILE_SIZE))
                    if not inventory[value - 10]:
                        screen.blit(lock, (j * TILE_SIZE + 20, q * TILE_SIZE + 20))
    return acids


# check for player collisions
def check_collisions():
    global level, inventory
    right_coord = int((player_x + 60) // 100)
    left_coord = int(player_x // 100)
    top_coord = int((player_y + 30) // 100)
    bot_coord = int((player_y + 80) // 100)
    top_right = level[top_coord][right_coord]
    bot_right = level[bot_coord][right_coord]
    top_left = level[top_coord][left_coord]
    bot_left = level[bot_coord][left_coord]
    if top_coord >= 0:
        if 0 < top_right < 4 or 0 < bot_right < 4:
            collide = 1
        elif 0 < top_left < 4 or 0 < bot_left < 4:
            collide = -1
        else:
            collide = 0
    elif bot_coord >= 0:
        if 0 < bot_right < 4:
            collide = 1
        elif 0 < bot_left < 4:
            collide = -1
        else:
            collide = 0
    else:
        collide = 0

    if 6 <= top_left <= 9:
        if not inventory[top_left - 6]:
            inventory[top_left - 6] = True
            # level[top_coord][left_coord] = 0
            key_sound.play()
    elif 6 <= top_right <= 9:
        if not inventory[top_right - 6]:
            key_sound.play()
            inventory[top_right - 6] = True
            # level[top_coord][right_coord] = 0

    elif 6 <= bot_left <= 9:
        if not inventory[bot_left - 6]:
            inventory[bot_left - 6] = True
            # level[bot_coord][left_coord] = 0
            key_sound.play()
    elif 6 <= bot_right <= 9:
        if not inventory[bot_right - 6]:
            inventory[bot_right - 6] = True
            # level[bot_coord][right_coord] = 0
            key_sound.play()

    doorways = [False, False, False, False]
    if 10 <= top_left <= 13:
        if inventory[top_left - 10]:
            doorways[top_left - 10] = True
    elif 10 <= top_right <= 13:
        if inventory[top_right - 10]:
            doorways[top_right - 10] = True
    elif 10 <= bot_left <= 13:
        if inventory[bot_left - 10]:
            doorways[bot_left - 10] = True
    elif 10 <= bot_right <= 13:
        if inventory[bot_right - 10]:
            doorways[bot_right - 10] = True

    return collide, doorways


# check feet collision on landings
def check_verticals():
    global player_y
    center_coord = int((player_x + 30) // 100)
    bot_coord = int((player_y + 110) // 100)
    if player_y + 110 > 0:
        if 0 < level[bot_coord][center_coord] < 4:
            falling = False
        else:
            falling = True
    else:
        falling = True
    if not falling:
        player_y = (bot_coord - 1) * 100 - 10
    return falling


def print_end(win_or_lose):
    global counter
    pygame.draw.rect(screen, 'black', [50, 50, WIDTH - 100, HEIGHT - 100], 0, 10)
    pygame.draw.rect(screen, 'white', [50, 50, WIDTH - 100, HEIGHT - 100], 10, 10)
    frame = frames[counter // 5]
    # Y
    screen.blit(frame, (70, 70))
    screen.blit(frame, (120, 170))
    screen.blit(frame, (170, 270))
    screen.blit(frame, (220, 170))
    screen.blit(frame, (270, 70))
    screen.blit(frame, (170, 370))
    # O
    screen.blit(frame, (450, 70))
    screen.blit(frame, (400, 170))
    screen.blit(frame, (400, 270))
    screen.blit(frame, (450, 370))
    screen.blit(frame, (500, 70))
    screen.blit(frame, (550, 170))
    screen.blit(frame, (550, 270))
    screen.blit(frame, (500, 370))
    # U
    screen.blit(frame, (650, 70))
    screen.blit(frame, (650, 170))
    screen.blit(frame, (650, 270))
    screen.blit(frame, (700, 370))
    screen.blit(frame, (800, 170))
    screen.blit(frame, (800, 270))
    screen.blit(frame, (800, 70))
    screen.blit(frame, (750, 370))
    font = pygame.font.Font('freesansbold.ttf', 380)
    win_text = font.render(win_or_lose, True, 'white')
    screen.blit(win_text, (100, 500))
    font = pygame.font.Font('freesansbold.ttf', 100)
    win_text2 = font.render(f'Your Time: {time * 2.5}', True, 'white')
    screen.blit(win_text2, (950, 100))
    win_text2 = font.render(f'Enter to Restart', True, 'white')
    screen.blit(win_text2, (950, 300))


# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    screen.blit(bg, (0, 0))
    if counter < 18:
        counter += 1
    else:
        counter = 1
    if not win and not lose:
        if second_count < 59:
            second_count += 1
        else:
            second_count = 0
            time += 1
    if lives > 0:
        lose = False
    else:
        lose = True

    # draw board tiles
    acid_list = draw_board(level)
    # draw player
    draw_player(counter, direction, mode)
    # draw inventory
    draw_inventory()
    if win:
        print_end('WIN!')
        end_sound.play(1)
    elif lose:
        print_end('LOSE!')
        end_sound.play(1)
    # handle x-direction movement
    if mode == 'walk':
        if direction == -1 and player_x > 0 and colliding != -1:
            player_x -= player_speed
        elif direction == 1 and player_x < WIDTH - 70 and colliding != 1:
            player_x += player_speed
    colliding, door_collisions = check_collisions()

    # jumping code
    if in_air:
        y_change -= gravity
        player_y -= y_change
    in_air = check_verticals()
    if not in_air:
        y_change = 0

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = -1
                mode = 'walk'
            if event.key == pygame.K_RIGHT:
                direction = 1
                mode = 'walk'
            if event.key == pygame.K_SPACE and not in_air:
                in_air = True
                y_change = jump_height
                jump_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and direction == -1:
                mode = 'idle'
            if event.key == pygame.K_RIGHT and direction == 1:
                mode = 'idle'
            if not win and not lose:
                if enter_message and event.key == pygame.K_RETURN:
                    for i in range(len(door_collisions)):
                        if door_collisions[i]:
                            if i != 3:
                                active_phase, player_coords = teleport(i, active_phase)
                                acid_list = []
                                player_x = player_coords[0] * 100
                                player_y = player_coords[1] * 100 - (8 * player_scale - 100)
                                level = levels[active_level][active_phase]
                                init_x = player_x
                                init_y = player_y
                                y_change = 0
                                portal_sound.play()
                            else:
                                if active_level < len(levels) - 1:
                                    active_level += 1
                                    portal_sound.play()
                                    key_sound.play(active_level)
                                else:
                                    win = True
                                level = levels[active_level][active_phase]
                                inventory = [False, False, False, False]
                                for _ in range(len(level)):
                                    if 5 in level[_]:
                                        start_pos = (_, level[_].index(5))
                                player_x = start_pos[1] * 100
                                player_y = start_pos[0] * 100 - (8 * player_scale - 100)
                                init_x = player_x
                                init_y = player_y
                                y_change = 0
            elif win or lose:
                active_level = 0
                active_phase = 3
                win = False
                lose = False
                time = 0
                level = levels[active_level][active_phase]
                inventory = [False, False, False, False]
                for _ in range(len(level)):
                    if 5 in level[_]:
                        start_pos = (_, level[_].index(5))
                player_x = start_pos[1] * 100
                player_y = start_pos[0] * 100 - (8 * player_scale - 100)
                init_x = player_x
                init_y = player_y
                y_change = 0
                lives = 5
                end_sound.stop()

    for i in range(len(acid_list)):
        if acid_list[i].collidepoint(player_x + 30, player_y + 20):
            lives -= 1
            player_x = init_x
            player_y = init_y
            acid_sound.play()

    if True in door_collisions:
        enter_message = True
    else:
        enter_message = False

    pygame.display.flip()
pygame.quit()
