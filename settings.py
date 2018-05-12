import pygame as pg
vec = pg.math.Vector2


# game settings
WIDTH = 64 * 20  
HEIGHT = 64 * 10 
FPS = 60
TITLE = "交大電資營神探"
TILESIZE = 64
GAMETIME = 60


# Player settings
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_SPEED = 3
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_HEALTH = 1000

# Weapon settings
BARREL_OFFSET = vec(30, 10)
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 1000
BULLET_RATE = 150
GUN_SPREAD = 5
DAMAGE = 20

# Mob settings
ZOMBIE_IMG = 'zombie1_hold.png'
ZOMBIE_SPEED = 1
ZOMBIE_HIT_RECT = pg.Rect(0, 0, 30, 30)
ZOMBIE_HEALTH = 100

# Treasure
TREASURE_IMG = 'treasure.png'


