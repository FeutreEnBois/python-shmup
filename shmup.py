# Shmup game
#
import pygame, sys, random
from pygame.locals import *
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Dimention window + FPS
WINDOWWIDTH = 1280
WINDOWHEIGHT = 1260
FPS = 60
POWERUP_TIME = 20000

# define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
THETHING = (255, 127, 0)

#Initialize pygame and create window
pygame.init()
pygame.mixer.init()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('test shooter')
mainClock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# def
def terminate():
    pygame.quit()
    sys.exit()
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, THETHING)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def newMob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGHT
    outline_rect = pygame.Rect(x,y,BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    windowSurface.blit(BACKGROUND, BACKGROUND_RECT)
    draw_text(windowSurface, "SHMUP !", 64, WINDOWWIDTH / 2, WINDOWHEIGHT /4)
    draw_text(windowSurface, "Mouse motion move, Mouse Button Left to fire", 22, WINDOWWIDTH /2, WINDOWHEIGHT / 2 )
    draw_text(windowSurface, "Press a key to begin", 18, WINDOWWIDTH / 2, WINDOWHEIGHT *3/4)
    draw_text(windowSurface, "topScore = %s" %(topScore), 18, WINDOWWIDTH /2, WINDOWHEIGHT * 2/3)
    pygame.display.flip()
    waiting = True
    while waiting:
        mainClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                waiting = False

# Class
class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(PLAYER_IMG, (50,38))
        self.image.set_colorkey(BLACK)
        self.radius = 20
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WINDOWWIDTH/2
        self.rect.bottom = WINDOWHEIGHT - 20
        self.shield = 50
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.lives = 2
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.control = True
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.control = True

        keystate = pygame.key.get_pressed()
        keystate_Mouse = pygame.mouse.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate_Mouse[0] == 1:
            self.shoot()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            if self.power == 1:
                self.last_shot = now
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                self.last_shot = now
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power == 3:
                self.last_shot = now
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                bullet3 = Bullet(self.rect.centerx, self.rect.top+10)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet3)
                shoot_sound.play()
            if self.power >= 4:
                self.last_shot = now
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                bullet3 = Bullet(self.rect.centerx, self.rect.top+10)
                bullet4 = Bullet(self.rect.centerx-20, self.rect.top)
                bullet5 = Bullet(self.rect.centerx+20, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet3)
                all_sprites.add(bullet4)
                bullets.add(bullet4)
                all_sprites.add(bullet4)
                bullets.add(bullet4)
                shoot_sound.play()

    def hide(self):
        self.control = False
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WINDOWWIDTH/2 , WINDOWHEIGHT + 200)




class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85/ 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WINDOWWIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(14,25)
        self.speedx = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > WINDOWHEIGHT +10 or self.rect.left < -25 or self.rect.right > WINDOWWIDTH +20:
            self.rect.x = random.randrange(0, WINDOWWIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-2, 2)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(LASER_IMG, (9, 38))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # Kill if it moves off the top of the screen
        if self.rect.top > WINDOWHEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size= size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 25

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center





# Load all game graphics
BACKGROUND = pygame.image.load(path.join(img_dir, "spaceBackground1.png")).convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOWWIDTH,WINDOWHEIGHT))
BACKGROUND_RECT = BACKGROUND.get_rect()
PLAYER_IMG = pygame.image.load(path.join(img_dir, 'playerShip2_orange.png')).convert()
player_mini_img = pygame.transform.scale(PLAYER_IMG, (25,19))
player_mini_img.set_colorkey(BLACK)
LASER_IMG = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png','meteorBrown_big2.png','meteorBrown_med1.png',
               'meteorBrown_med3.png','meteorBrown_small1.png','meteorBrown_tiny1.png',
               'meteorGrey_med1.png','meteorGrey_med2.png','meteorGrey_small2.png',]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0%s.png' %(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32,32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0%s.png' %(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_img = {}
powerup_img['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_img['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

# Load all game sound
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Pew__009.ogg'))
shoot_sound.set_volume(0.1)
explosion_sound = []
for snd in ['Explosion__006.ogg', 'Explosion3__002.ogg', 'Explosion3__006.ogg']:
    explosion_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'boss.ogg'))
pygame.mixer.music.set_volume(0.6)
player_die_snd = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
player_die_snd.set_volume(0.4)


pygame.mixer.music.play(-1, 0.0)
topScore = 0
#Game loop
game_over = True
while True:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        for i in range(160):
            newMob()

        score = 0
    # keep loop running at the same speed
    mainClock.tick(FPS)
    #process input (events)
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()

        if event.type == MOUSEMOTION and player.control == True:
            player.rect.centerx = event.pos[0]
            player.rect.centery = event.pos[1]

    #update
    all_sprites.update()
    # check if a bullet hit a mob
    # check if a mob hit the player
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        expl_snd = random.choice(explosion_sound)
        expl_snd.set_volume(0.1)
        expl_snd.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.97:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newMob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in  hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newMob()
        if player.shield <= 0 :
            player_die_snd.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
        #if the player died and the explosion has finished playing end the game
    if player.lives == 0 and not death_explosion.alive():
        if score > topScore:
            topScore = score
        game_over = True

    # check si le joueur touche un powerups
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    #draw / render
    windowSurface.fill(WHITE)
    windowSurface.blit(BACKGROUND, BACKGROUND_RECT)
    all_sprites.draw(windowSurface)
    # draw_text = (surface, text, font size, x, y)
    draw_text(windowSurface, str(score), 30, WINDOWWIDTH / 2, 10)
    draw_shield_bar(windowSurface, 5, 5,player.shield) # surface, x, y, % de bar a remplir
    draw_lives(windowSurface, WINDOWWIDTH -100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()














