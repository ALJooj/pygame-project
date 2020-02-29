import pygame
import os
import random
import sys

# init
pygame.init()

# options

pygame.display.set_caption('path of path')
size = width, height = (700, 700)
screen = pygame.display.set_mode(size)
fps = 50
tile_width = tile_height = 100
clock = pygame.time.Clock()


# funcs

# load img
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# terminate
def terminate():
    pygame.quit()
    sys.exit()


def count(counter):
    if counter > 200:
        return counter - 200
    return counter + 1


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('start_fon.png'), (width, height))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        pygame.display.flip()
        clock.tick(fps)


# load level
def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [s.strip() for s in mapFile]
    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# generate level
def generate_level(level):
    enemies = 0
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level)):
            if level[y][x] == '.':
                Tile(x, y)
            elif level[y][x] == '@':
                Tile(x, y)
                new_player = Player(0, x, y)
            elif level[y][x] == '#':
                enemies += 1
                Tile(x, y)
                Enemy(x, y)
            elif level[y][x] == '$':
                enemies += 1
                Tile(x, y)
                BigEnemy(x, y)
            elif level[y][x] == 'R':
                Tile(x, y)
                Rune(x, y)
            elif level[y][x] == 'D':
                Tile(x, y)
                DragonMage(x, y)
    return new_player, x + 1, y + 1, enemies


# textures
# разновидности пола (повторение для соотношение 1:2 текстур)
tile_images = [
    pygame.transform.scale(load_image('floor1.png'), (tile_width, tile_height)),
    pygame.transform.scale(load_image('floor2.png'), (tile_width, tile_height)),
    pygame.transform.scale(load_image('floor2.png'), (tile_width, tile_height))
]
# игрок
player_image = [
    pygame.transform.scale(load_image('mainhero_front.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('mainhero_left.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('mainhero_back.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('mainhero_right.png', -1), (tile_width, tile_height)),
]
# враг
enemy_image = [
    pygame.transform.scale(load_image('knight_12.png', -1), (tile_width, tile_height)),
    # attack 1 - 10
    pygame.transform.scale(load_image('knight_12.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_1.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_3.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_4.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_5.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_1.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('knight_12.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('knight_12.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('knight_12.png', -1), (tile_width, tile_height)),

    # moving 10 - 13 l
    pygame.transform.scale(load_image('enemy/moving/e_move_1.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/moving/e_move_2.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/moving/knight_12.png', -1), (tile_width, tile_height)),
    # moving 13 - 17 r
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/moving/e_move_1.png', -1), (tile_width, tile_height)), True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/moving/e_move_2.png', -1), (tile_width, tile_height)), True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/moving/knight_12.png', -1), (tile_width, tile_height)), True, False),
]

# Большой враг
b_e_t_height = int(tile_height * 1.23)
big_enemy_image = [
    pygame.transform.scale(load_image('big_enemy.png', -1), (tile_width, b_e_t_height)),
    # attack 1 - 14
    pygame.transform.scale(load_image('big_enemy.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy/attack/attack_1.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy/attack/attack_2.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy/attack/attack_3.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy/attack/attack_4.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy/attack/attack_5.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy/attack/attack_6.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy/attack/attack_7.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy/attack/attack_8.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy.png', -1), (tile_width, b_e_t_height)),
    pygame.transform.scale(load_image('big_enemy.png', -1), (tile_width, b_e_t_height)),
    # moving 14 - 17 l
    pygame.transform.flip(
        pygame.transform.scale(load_image('big_enemy/moving/moving_1.png', -1), (tile_width, int(tile_height * 1.23))),
        True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('big_enemy/moving/moving_2.png', -1), (tile_width, int(tile_height * 1.23))),
        True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('big_enemy/moving/moving_3.png', -1), (tile_width, int(tile_height * 1.23))),
        True, False),
    # moving 17 - 21 r
    pygame.transform.scale(load_image('big_enemy/moving/moving_1.png', -1), (tile_width, int(tile_height * 1.23))),
    pygame.transform.scale(load_image('big_enemy/moving/moving_2.png', -1), (tile_width, int(tile_height * 1.23))),
    pygame.transform.scale(load_image('big_enemy/moving/moving_3.png', -1), (tile_width, int(tile_height * 1.23))),
    pygame.transform.scale(load_image('big_enemy.png', -1), (tile_width, int(tile_height * 1.23))),
]

# Дракон Маг
d_t_width = int(1.25 * tile_width)
dragon_image = [
    pygame.transform.scale(load_image('dragon.png', -1), (d_t_width * 2, tile_height * 2)),
    # attack 1 - 12
    pygame.transform.scale(load_image('dragon/attack_1.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon/attack_2.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon/attack_3.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon/attack_3.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon/attack_2.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon/attack_2.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon/attack_1.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon.png', -1), (d_t_width * 2, tile_width * 2)),
    pygame.transform.scale(load_image('dragon.png', -1), (d_t_width * 2, tile_width * 2)),
]

# classes


# стенка для ограничения карты
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.transform.scale(load_image('grass.png'), [1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.transform.scale(load_image('grass.png'), [x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class YouWon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game_group)
        self.image = pygame.transform.scale(load_image('winning_screen.jpg'), size)
        self.rect = self.image.get_rect()
        self.rect.x = 2 * width

    def update(self):
        if self.rect.x >= 0:
            self.rect = self.rect.move(-8, 0)
        else:
            pygame.time.wait(6666)
            terminate()


# скрин смерти (проигрыш)
class YouLost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game_group)
        self.image = pygame.transform.scale(load_image('gameover_screen.png'), size)
        self.rect = self.image.get_rect()
        self.rect.x = -width

    def update(self):
        if self.rect.x <= 0:
            self.rect = self.rect.move(8, 0)
        else:
            pygame.time.wait(4666)
            terminate()


# могила для смерти врага
class Grave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, grave_group)
        w = (tile_width // 2) + tile_width // 4      # |  размеры
        h = (tile_height // 2) + tile_height // 4    # |  размеры
        self.image = pygame.transform.scale(load_image('grave.png', -1), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x     # установка
        self.rect.y = y


# призрак помогающий герою
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, ghost_group)
        self.image = pygame.transform.scale((load_image('ghost.png', -1)), (tile_width, tile_width))
        self.rect = self.image.get_rect().move(x, y)
        self.healthpoints = 3    # количество жизней
        self.attack_points = 2   # урон
        self.speed = 3           # скорость передвижения по карте
        self.r = 4 * tile_width  # радуис для обнаружения врага

    def check_for_enemy(self, enemy):
        x = self.rect.x + (tile_width // 2)
        y = self.rect.y + (tile_height // 2)
        rect = CheckForPlayer(x, y, self.r)
        if pygame.sprite.collide_rect(rect, enemy):  # проверка есть ли пресечение с врагом
            return True

    def chase_the_enemy(self, enemy):
        if self.check_for_enemy(enemy):
            x1 = enemy.rect.x + (tile_width // 2)
            y1 = enemy.rect.y - (tile_height // 2)
            x = self.rect.x + (tile_width // 2)
            y = self.rect.y - (tile_height // 2)
            if not abs(x1 - x) <= 65 or not abs(y1 - y) <= 65:  # остановка перед моделькой врага
                # способы передвижения
                if x1 < x:
                    if y1 > y:
                        self.rect = self.rect.move((-self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((-self.speed, -self.speed))
                #
                if x1 > x:
                    if y1 > y:
                        self.rect = self.rect.move((self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((self.speed, -self.speed))
                        #
                if y == y1:
                    if x1 > x:
                        self.rect = self.rect.move((self.speed, 0))
                    if x1 < x:
                        self.rect = self.rect.move((-self.speed, 0))

                elif x == x1:
                    if y1 > y:
                        self.rect = self.rect.move((0, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((0, -self.speed))
            else:
                return True

    def chase_the_player(self, enemy):
        x1 = enemy.rect.x + (tile_width // 2)
        y1 = enemy.rect.y - (tile_height // 2)
        x = self.rect.x + (tile_width // 2)
        y = self.rect.y - (tile_height // 2)
        if not abs(x1 - x) <= tile_width or not abs(y1 - y) <= tile_height:  # остановка перед моделькой врага
            # способы передвижения
            if x1 < x:
                if y1 > y:
                    self.rect = self.rect.move((-self.speed, self.speed))
                if y1 < y:
                    self.rect = self.rect.move((-self.speed, -self.speed))
            #
            if x1 > x:
                if y1 > y:
                    self.rect = self.rect.move((self.speed, self.speed))
                if y1 < y:
                    self.rect = self.rect.move((self.speed, -self.speed))
                    #
            if y == y1:
                if x1 > x:
                    self.rect = self.rect.move((self.speed, 0))
                if x1 < x:
                    self.rect = self.rect.move((-self.speed, 0))

            elif x == x1:
                if y1 > y:
                    self.rect = self.rect.move((0, self.speed))
                if y1 < y:
                    self.rect = self.rect.move((0, -self.speed))

    def check_healthpoints(self):   # жив ли
        if self.healthpoints <= 0:
            self.kill()

    def attack(self, enemy, counter):
        if counter % 80 == 0:   # задержка между атаками
            enemy.healthpoints -= self.attack_points


# класс клетки
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, tiles_group)
        self.image = tile_images[random.randint(0, len(tile_images) - 1)]   # рандомное заполнение
        self.rect = self.image.get_rect().move(tile_width * x + 10, tile_height * y + 5)


# mist coil spell
class MistCoil(pygame.sprite.Sprite):
    def __init__(self, pos, nav, attack):
        super().__init__(all_sprites, skill_group)
        self.image = pygame.transform.scale(load_image('magic.png', -1), (32, 32))
        self.rect = self.image.get_rect()
        self.attack = attack
        self.rect.x = pos[0] + (tile_width // 2 - 16)
        self.rect.y = pos[1]
        self.nav = nav

    def update(self, groups):
        if groups == hero_group:
            return
        for sprite in groups:
            if pygame.sprite.collide_rect(self, sprite):
                if type(sprite) == Enemy or type(sprite) == BigEnemy or type(sprite) == DragonMage:
                    sprite.healthpoints -= self.attack
                self.kill()

    def moving(self):
        if self.nav == 0:
            self.rect = self.rect.move((0, 14))
        if self.nav == 1:
            self.rect = self.rect.move((-14, 0))
        if self.nav == 2:
            self.rect = self.rect.move((0, -14))
        if self.nav == 3:
            self.rect = self.rect.move((14, 0))


# rune
class Rune(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, rune_group)
        self.image = pygame.transform.scale(load_image('rune.jpg', -1), (tile_width, tile_height))
        self.rect = self.image.get_rect().move(tile_width * x + 10, tile_height * y + 5)
        self.effect = random.choice(['attack', 'health', 'speed', 'max_dummies', 'mana'])


# player
class Player(pygame.sprite.Sprite):

    def __init__(self, pos_type, x, y):
        super().__init__(all_sprites, hero_group)
        self.pos_type = pos_type               # направление взгляда
        self.image = player_image[pos_type]    # загрузка нужного направления
        self.r = 210                           # радиус обнаружения могил
        self.max_counter = 300                 # максимальная мана
        self.haste_counter = 0
        self.max_dummies = 2                   # максимально кол-во одновременно призванных духов
        self.haste_used = False
        self.counter = self.max_counter // 2   # счетчик
        self.attack = 2                        # урон с койла
        self.max_hp = 8                        # максимальное хп
        self.healthpoints = self.max_hp        # кол-во жизней в данный момент
        self.speed = 3                         # показатель скорость
        self.rect = self.image.get_rect().move(tile_width * x + 10, tile_height * y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def use_effects(self, effect):
        if effect == 'health':
            self.max_hp += 2
            self.healthpoints += 2
        elif effect == 'attack':
            self.attack += 1
        elif effect == 'max_dummies':
            self.max_dummies += 1
        elif effect == 'mana':
            self.max_counter += 50
        else:
            self.speed += 1

    # проверка столкновений
    def collisions(self, sprite):
        global all_effects
        if type(sprite) == Rune and pygame.sprite.collide_mask(self, sprite):
                effect = sprite.effect
                all_effects.append(effect)
                sprite.kill()
                if effect == 'health':
                    self.max_hp += 2
                    self.healthpoints += 2
                elif effect == 'attack':
                    self.attack += 1
                elif effect == 'max_dummies':
                    self.max_dummies += 1
                elif effect == 'mana':
                    self.max_counter += 50
                else:
                    self.speed += 1

        if not self.haste_used or type(sprite) == Border:
            if pygame.sprite.collide_mask(self, sprite):
                if self.pos_type == 0:
                    self.rect = self.rect.move((0, -6))
                if self.pos_type == 1:
                    self.rect = self.rect.move((6, 0))
                if self.pos_type == 2:
                    self.rect = self.rect.move((0, 6))
                if self.pos_type == 3:
                    self.rect = self.rect.move((-6, 0))

    # хотьбя
    def go_right(self):
        self.image = player_image[3]
        self.pos_type = 3
        self.rect = self.rect.move(self.speed, 0)

    def go_left(self):
        self.image = player_image[1]
        self.pos_type = 1
        self.rect = self.rect.move(-self.speed, 0)

    def go_up(self):
        self.image = player_image[2]
        self.pos_type = 2
        self.rect = self.rect.move(0, -self.speed)

    def go_down(self):
        self.image = player_image[0]
        self.pos_type = 0
        self.rect = self.rect.move(0, self.speed)

    def moving(self, pos):
        w, h = pos[0] - self.rect.x or 1, pos[1] - self.rect.y or 1
        parts = abs(h) + abs(w)
        speed_x = (w * self.speed) / parts
        speed_y = (h * self.speed) / parts
        if speed_y > 0 and speed_y > speed_x:
            self.pos_type = 0
        else:
            self.pos_type = 2
        if speed_x > 0:
            self.pos_type = 3
        else:
            self.pos_type = 1
        self.rect = self.rect.move(speed_x, speed_y)

    def check_healthpoints(self):       # жив ли
        if self.healthpoints <= 0:
            self.kill()
            return True

    def cast_mist_coil(self):           # выпускание магического заряда
        if self.counter > 84:           # задержка
            MistCoil((self.rect.x, self.rect.y), self.pos_type, self.attack)
            self.counter -= 84

    def haste(self):                    # ускорение...
        if self.counter > 213:
            self.speed += 4
            self.haste_used = True
            self.counter -= 213

    def raise_the_dead(self, grave):    # призыв духов
        if self.counter > 149:          # проверка перезарядка
            x = self.rect.x + (tile_width // 2)
            y = self.rect.y + (tile_height // 2)
            rect = CheckForPlayer(x, y, self.r)
            if pygame.sprite.collide_rect(rect, grave):
                self.counter -= 149
                return True

    def count(self):
        if self.counter < self.max_counter:
            self.counter += 1
        if self.haste_used:
            if self.haste_counter == 90:
                self.speed -= 4
                self.haste_counter = 0
                self.haste_used = False
            self.haste_counter += 1


# нужный класс для "видения" персонажей
class CheckForPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, r):
        super().__init__()
        self.image = pygame.Surface([r, r])
        r1 = r // 2 - (tile_width // 2)
        r2 = r // 2 - (tile_height // 2)
        self.rect = self.image.get_rect().move(x - r1, y - r2)


# Enemy
class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__(all_sprites, enemy_group)
        self.frames = enemy_image[:]        # кадры для анимации
        self.attack_frames_l = enemy_image[1:10]
        self.moving_frames_l = enemy_image[10:13]
        self.moving_frames_r = enemy_image[13:17]
        #
        self.healthpoints = 6           # хп
        self.attack_points = 1          # урон
        self.speed = 1                  # скорость
        self.space = 0
        #
        self.cur_frame = 0              #
        self.attack_cur_frame_l = 0     # счетчики
        self.moving_cur_frame_l = 0     #
        self.moving_cur_frame_r = 0     #
        #
        self.r = 5 * tile_height        # радиус зрения
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 8)

    # анимация передвижения
    def update(self, counter):
        if counter % 7 == 0:
            self.attack_cur_frame_l = (self.attack_cur_frame_l + 1) % (len(self.attack_frames_l))
            self.image = self.attack_frames_l[self.attack_cur_frame_l]

    # функция для обнаружения героя врагами
    def check_for_player(self, sprite):
        x = self.rect.x  # + (tile_width // 2)
        y = self.rect.y  # + (tile_height // 2)
        rect = CheckForPlayer(x, y, self.r)
        if pygame.sprite.collide_rect(rect, sprite):
            return True

    # приследование
    def chase_the_player(self, sprite, counter):
        if self.check_for_player(sprite):
            x1 = sprite.rect.x + (tile_width // 2)
            y1 = sprite.rect.y + (tile_height // 2)
            x = self.rect.x + (tile_width // 2)
            y = self.rect.y + (tile_height // 2)
            if not abs(x1 - x) <= tile_width * 0.95 or not abs(y1 - y) <= tile_height * 0.95 + self.space:  # остановка перед героями
                #  движения и смена анимация
                if x1 < x:
                    if counter % 16 == 0:
                        self.moving_cur_frame_l = (self.moving_cur_frame_l + 1) % len(self.moving_frames_l)
                        self.image = self.moving_frames_l[self.moving_cur_frame_l]
                    if y1 > y:
                        self.rect = self.rect.move((-self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((-self.speed, -self.speed))
                #
                if x1 > x:
                    if counter % 16 == 0:
                        self.moving_cur_frame_r = (self.moving_cur_frame_r + 1) % len(self.moving_frames_r)
                        self.image = self.moving_frames_r[self.moving_cur_frame_r]
                    if y1 > y:
                        self.rect = self.rect.move((self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((self.speed, -self.speed))
                #
                if y == y1:
                    if x1 > x:
                        self.rect = self.rect.move((self.speed, 0))
                    if x1 < x:
                        if counter % 16 == 0:
                            self.moving_cur_frame_l = (self.moving_cur_frame_l + 1) % len(self.moving_frames_l)
                            self.image = self.moving_frames_l[self.moving_cur_frame_l]
                        self.rect = self.rect.move((-self.speed, 0))
                #
                elif x == x1:
                    if counter % 16 == 0:
                        self.moving_cur_frame_l = (self.moving_cur_frame_l + 1) % len(self.moving_frames_l)
                        self.image = self.moving_frames_l[self.moving_cur_frame_l]
                    if y1 > y:
                        self.rect = self.rect.move((0, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((0, -self.speed))
            else:
                return True

    def check_healthpoints(self):       # смерть врага и образование могилки на его месте
        if self.healthpoints <= 0:
            Grave(self.rect.x, self.rect.y)
            self.kill()

    def attack(self, sprite, counter):           # атака
        if counter % 63 == 0:
            sprite.healthpoints -= self.attack_points


# big enemy

class BigEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.healthpoints = 8
        self.speed = 4
        self.attack_points = 2
        self.r = 7 * tile_height
        self.space = 23
        self.frames = big_enemy_image[:]  # кадры для анимации
        self.attack_frames_l = big_enemy_image[1:14]
        self.moving_frames_l = big_enemy_image[14:17]
        self.moving_frames_r = big_enemy_image[17:21]
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 8)

    def attack(self, sprite, counter):           # атака
        if counter % 95 == 0:
            sprite.healthpoints -= self.attack_points

    def update(self, counter):
        if counter % 7 == 0:
            self.attack_cur_frame_l = (self.attack_cur_frame_l + 1) % (len(self.attack_frames_l))
            self.image = self.attack_frames_l[self.attack_cur_frame_l]


#
class DragonMage(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.healthpoints = 50
        self.speed = 0
        self.attack_points = 4
        self.r = 8 * tile_height
        self.space = tile_height
        self.frames = dragon_image[:]                # кадры для анимации
        self.attack_frames_l = dragon_image[1:12]
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 8)

    def attack(self, sprite, counter):           # атака
        if counter % 165 == 0:
            MageThrow(self.rect.x + (tile_width // 5), self.rect.y + tile_height,
                      self.speed_x, self.speed_y, self.attack_points)

    def update(self, counter):
        if counter % 6 == 0:
            self.attack_cur_frame_l = (self.attack_cur_frame_l + 1) % (len(self.attack_frames_l))
            self.image = self.attack_frames_l[self.attack_cur_frame_l]

    def chase_the_player(self, sprite, counter):
        if self.check_for_player(sprite):
            self.r = 13 * tile_height
            x1 = random.choice([
                sprite.rect.x + (tile_width // 2),
                sprite.rect.x - (tile_width // 2),
                sprite.rect.x - tile_width
            ])
            y1 = sprite.rect.y + (tile_height // 3)
            x = self.rect.x + (tile_width // 5)
            y = self.rect.y + tile_height
            self.balls_speed = 50
            self.speed_x = (x1 - x) // self.balls_speed
            self.speed_y = (y1 - y) // self.balls_speed
            return True


# Mage ball
class MageThrow(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y, damage):
        super().__init__(skill_group)
        self.image = pygame.transform.scale(load_image('mage_throw.png', -1), (tile_width // 3, tile_height // 3))
        self.rect = self.image.get_rect().move(x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.attack = damage

    def moving(self):
        self.rect = self.rect.move(self.speed_x, self.speed_y)

    def update(self, groups):
        if groups != enemy_group:
            for sprite in groups:
                if pygame.sprite.collide_mask(self, sprite):
                    if type(sprite) == Player or type(sprite) == Ghost:
                        sprite.healthpoints -= self.attack
                    self.kill()


# Ui
class UserInterface(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game_group)
        self.image = pygame.transform.scale(load_image('UI.png', (255, 255, 255)),
                                            (int(1.75 * tile_width * 1.5), int(1.5 * tile_height)))
        self.rect = self.image.get_rect()
        # self.rect.bottom = height


# camera
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


start_screen()
LEVELS = ['0.txt', '1.txt', '2.txt', '3.txt', '4.txt']
all_effects = []

# генерация уровней в случаи победы

for level in LEVELS:
    # groups
    all_sprites = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    rune_group = pygame.sprite.Group()
    skill_group = pygame.sprite.Group()
    grave_group = pygame.sprite.Group()
    ghost_group = pygame.sprite.Group()
    game_group = pygame.sprite.Group()

    # generating level
    counter = 0
    camera = Camera()
    gm_lost = YouLost()
    ui_2 = UserInterface()
    ui_2.rect.bottom = height + 75
    ui_2.rect.x = 245
    ui = UserInterface()
    ui.rect.bottom = height
    fon = pygame.transform.scale(load_image('lava.png'), (700, 700))
    player, level_x, level_y, enemies = generate_level(load_level(level))
    for effect in all_effects:
        player.use_effects(effect)

    # границы уровня
    Border(0, 0, level_x * tile_width, 0)                                           #
    Border(0, level_y * tile_height, level_x * tile_width, level_y * tile_height)   #
    Border(0, 0, 0, level_x * tile_width)                                           #
    Border(level_x * tile_width, 0, level_x * tile_width, level_y * tile_height)    #

    # allowing flags
    running = True
    key_down = False
    dead_raised = False
    key = ''
    delta_len = 0
    start_time = None
    attacked = False
    game_over = False
    #
    clicked = False
    #
    font_1 = pygame.font.SysFont('castellar', 22)
    font_2 = pygame.font.SysFont('castellar', 22)

    # текст скиллов
    string_rendered_1 = font_2.render(' 8.4', 1, pygame.Color('white'))
    string_rendered_2 = font_2.render('21.3', 1, pygame.Color('white'))
    string_rendered_3 = font_2.render('14.9', 1, pygame.Color('white'))
    # текст статов
    string_rendered_5 = font_2.render('Speed:', 1, pygame.Color('white'))
    string_rendered_6 = font_2.render('Max Dummies:', 1, pygame.Color('white'))

    # main loop
    while running:
        if len(enemy_group) == 0:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                last_pos = event.pos

                clicked = True
            if event.type == pygame.MOUSEMOTION and clicked:
                last_pos = event.pos

                # player.moving(event.pos)
            if event.type == pygame.KEYDOWN:
                key = event.key
                key_down = True
                if event.key == pygame.K_d:
                    for sprite in enemy_group:
                        sprite.healthpoints -= 1
                # скилы (способности)
                if event.key == pygame.K_z:
                    player.cast_mist_coil()
                if event.key == pygame.K_x:
                    player.haste()
                if event.key == pygame.K_c:
                    for grave in grave_group:
                        if player.max_dummies >= len(ghost_group) + 1:
                            if player.raise_the_dead(grave):
                                Ghost(grave.rect.x, grave.rect.y)
                                grave.kill()


            if event.type == pygame.KEYUP:
                key_down = False

        # изменяем ракурс камеры
        camera.update(player)

        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        # логика врага
        for enemy in enemy_group:
            enemy.check_healthpoints()
            if enemy.chase_the_player(player, counter):
                enemy.attack(player, counter)
                enemy.update(counter)
            else:
                enemy.attack_cur_frame = -1
            for ghost in ghost_group:
                if enemy.chase_the_player(ghost, counter):
                    enemy.attack(ghost, counter)
                    enemy.update(counter)
                    break

        # логика призрака
        for ghost in ghost_group:
            ghost.check_healthpoints()
            for enemy in enemy_group:
                if ghost.chase_the_enemy(enemy):
                    ghost.attack(enemy, counter)
                    break
                else:
                    ghost.chase_the_player(player)
        # взаимодействия "койла"
        for sprite in (vertical_borders, horizontal_borders, enemy_group, hero_group):
            skill_group.update(sprite)

        # полет "койла"
        for sprite in skill_group:
            sprite.moving()

        # логика "призыва мертвых"
        if dead_raised:
            for grave in grave_group:
                if player.max_dummies >= len(ghost_group) + 1:
                    if player.raise_the_dead(grave):
                        Ghost(grave.rect.x, grave.rect.y)
                        grave.kill()
                        dead_raised = False

        # "плавное" движение
        if key_down:
            if key == pygame.K_RIGHT:
                player.go_right()
            if key == pygame.K_LEFT:
                player.go_left()
            if key == pygame.K_UP:
                player.go_up()
            if key == pygame.K_DOWN:
                player.go_down()

        # moving
        if clicked:
            player.moving(last_pos)

        # прорисовка текстур
        screen.blit(fon, (0, 0))

        tiles_group.draw(screen)
        rune_group.draw(screen)
        grave_group.draw(screen)
        ghost_group.draw(screen)
        enemy_group.draw(screen)
        skill_group.draw(screen)
        hero_group.draw(screen)
        game_group.draw(screen)

        # столкновения игрока
        for sprite in (*enemy_group, *vertical_borders, *horizontal_borders, *rune_group):
            player.collisions(sprite)

        # проверка смерти
        if player.check_healthpoints():
            gm_lost.update()

        # отоброжение маны
        string_rendered = font_1.render('Health: ' + str(player.healthpoints) + '/' + str(player.max_hp),
                                        1, pygame.Color('red'))
        screen.blit(string_rendered, (26, height - 139))
        # отоброжение маны
        string_rendered = font_1.render('Mana: ' + str(player.counter / 10) + '/' + str(player.max_counter / 10)
                                        , 1, pygame.Color('blue'))
        screen.blit(string_rendered, (26, height - 120))
        # raise the dead info
        screen.blit(string_rendered_1, (25, height - 95))
        # haste info
        screen.blit(string_rendered_2, (25 + 80, height - 95))   # height - 57
        # mist coil info
        screen.blit(string_rendered_3, (25 + 160, height - 95))

        # raise the dead info
        string_rendered = font_2.render('Damage: ' + str(player.attack),
                                        1, pygame.Color('white'))
        screen.blit(string_rendered, (260, height - 66))
        # haste info
        string_rendered = font_2.render('Speed: ' + str(player.speed),
                                        1, pygame.Color('white'))
        screen.blit(string_rendered, (260, height - 44))
        # mist coil info
        string_rendered = font_2.render('Max Dummies: ' + str(len(ghost_group)) + '/' + str(player.max_dummies),
                                        1, pygame.Color('white'))
        screen.blit(string_rendered, (260, height - 22))

        player.count()
        counter = count(counter)
        pygame.display.flip()
        clock.tick(fps)


winning = YouWon()
while True:
    winning.update()
    game_group.draw(screen)
    pygame.display.flip()
    clock.tick(fps)