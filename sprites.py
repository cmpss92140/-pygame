import pygame as pg
from random import uniform
from settings import *
from tilemap import collide_hit_rect
import math
vec = pg.math.Vector2

def got_hit(sprite, group):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        sprite.health -= DAMAGE
        if isinstance(hits[0], Bullet):
                hits[0].kill()
        if sprite.health < 0 and isinstance(sprite, Player):
            sprite.game.win = False
            sprite.game.playing = False

def collide(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            elif hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.hit_rect.centerx = sprite.pos.x
            sprite.vel.x = 0
            if isinstance(hits[0], Treasure):
                sprite.game.win = True
                sprite.game.playing = False
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            elif hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.hit_rect.centery = sprite.pos.y
            sprite.vel.y = 0
            if isinstance(hits[0], Treasure):
                sprite.game.win = True
                sprite.game.playing = False

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.rot = 0
        self.health = PLAYER_HEALTH
        self.last_shot = 0
        
    def get_mouse(self):
        self.mouse_pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.pos[0] -= 3
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.pos[0] += 3
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.pos[1] -= 3
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.pos[1] += 3

    def get_angle(self):
        direction = self.mouse_pos - self.game.camera.pos - self.pos
        return math.atan2(-direction[1],direction[0])

    def update(self):
        self.get_keys()
        self.get_mouse()
        self.rot = self.get_angle() * 180 / math.pi 
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        collide(self, self.game.treasures, 'x')
        collide(self, self.game.treasures, 'y')
        self.hit_rect.centerx = self.pos.x
        collide(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide(self, self.game.walls, 'y')
        self.rect.center = self.pos
        got_hit(self, self.game.zombies)

    def draw_health(self):
        if self.health > 800:
            col = (0,255,0)
        elif self.health > 300:
            col = (0,255,255)
        else:
            col = (255,0,0)
        width = int(self.rect.width * self.health / PLAYER_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < PLAYER_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Zombie(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.zombies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombie_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = ZOMBIE_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.rot = 0
        self.health = ZOMBIE_HEALTH
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.zombie_img, self.rot)
        self.rect = self.image.get_rect()
        move = (self.game.player.pos - self.pos)
        move.x, move.y = ZOMBIE_SPEED *  move.x / math.sqrt(move.x ** 2 + move.y ** 2), ZOMBIE_SPEED * move.y / math.sqrt(move.x ** 2 + move.y ** 2)
        self.pos += move
        self.hit_rect.centerx = self.pos.x
        collide(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        got_hit(self, self.game.bullets)
        if self.health <= 0:
            self.kill()
    
    def draw_health(self):
        if self.health > 60:
            col = (0,255,0)
        elif self.health > 30:
            col = (0,255,255)
        else:
            col = (255,0,0)
        width = int(self.rect.width * self.health / ZOMBIE_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < ZOMBIE_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class Treasure(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.treasures
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.treasure_img
        self.game = game
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.rect.center = vec(x,y)

    def update(self):
        self.image = pg.transform.rotate(self.game.treasure_img, 0)
        self.rect = self.image.get_rect()
        collide(self, self.game.walls, 'x')
        collide(self, self.game.walls, 'y')
        self.rect.center = self.pos

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y