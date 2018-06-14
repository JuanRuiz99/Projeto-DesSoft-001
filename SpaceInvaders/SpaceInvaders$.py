# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 20:34:54 2018

@author: leo72
"""

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

width = 480
height = 600
fps = 60
tempo_poder = 5000

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Meteor Destroyer")
clock = pygame.time.Clock()

fonte_nome = pygame.font.match_font('arial')
def texto_tela(surf, text, size, x, y):
    fonte = pygame.font.Font(fonte_nome, size)
    text_surface = fonte.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newenemie():
    e = Enemies()
    sprites.add(e)
    enemies.add(e)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    Bar_lenght = 100
    Bar_height = 10
    fill = (pct / 100) * Bar_lenght
    outline_rect = pygame.Rect(x, y, Bar_lenght, Bar_height)
    fill_rect = pygame.Rect(x, y, fill, Bar_height)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)
    
#vidas
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
#
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 20
        #desenhar o circulo vermelho pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        #vidas
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        #
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        
    def update(self):
        #tempo do poder
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > tempo_poder:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            
        #vidas unhide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10
        #
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
            
    def poder(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
                
            
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                tiro = Tiro(self.rect.centerx, self.rect.top)
                sprites.add(tiro)
                tiros.add(tiro)
                tiro_som.play()
            if self.power >= 2:
                tiro = Tiro(self.rect.centerx, self.rect.top)
                tiro1 = Tiro(self.rect.left, self.rect.centery)
                tiro2 = Tiro(self.rect.right, self.rect.centery)
                sprites.add(tiro)
                sprites.add(tiro1)
                sprites.add(tiro2)
                tiros.add(tiro)
                tiros.add(tiro1)
                tiros.add(tiro2)
                tiro_som.play()
                    
    #vidas
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, height + 200)
    #        
    
class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_real = random.choice(meteor_images)
        self.image_real.set_colorkey(black)
        self.image = self.image_real.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
       #desenhar o circulo vermelho pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(3, 10 )
        self.speedx = random.randrange(-3, 3)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_real, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 15)

class Tiro(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image.set_colorkey(black) 
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        #apaga se passar do topo da tela
        if self.rect.bottom < 0:
            self.kill()
            
class Poder(pygame.sprite.Sprite):
    def __init__ (self, center):
        pygame.sprite.Sprite.__init__(self)
        if player.power >= 3:
            self.type = 'shield'
            self.image = poder_imagens[self.type]
            self.image.set_colorkey(black) 
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.speedy = 5
            
        elif player.power == 2:
            self.type = random.choice(['shield', 'shield', 'gun'])
            self.image = poder_imagens[self.type]
            self.image.set_colorkey(black) 
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.speedy = 5
            
        else:
            self.type = random.choice(['shield', 'gun'])
            self.image = poder_imagens[self.type]
            self.image.set_colorkey(black) 
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.speedy = 5
    
    def update(self):
        self.rect.y += self.speedy
        #apaga se passar do topo da tela
        if self.rect.top > height:
            self.kill()
        
class Explosao(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = animacaoexplosao[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
   
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(animacaoexplosao[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = animacaoexplosao[self.size][self.frame]
                self.rect.center = center

def gameover_screen():
    screen.fill(black)
    texto_tela(screen, "Meteor Destroyer", 64, width / 2, height / 4)
    texto_tela(screen, "Arrows keys move, Space to fire", 22, width / 2, height / 2)
    texto_tela(screen, "Press a key to begin", 18, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
        
#imagens
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'Ship.png')).convert()

#vidas
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(black)
#

#meteor_img = pygame.image.load(path.join(img_dir, 'Meteor.png')).convert()
laser_img = pygame.image.load(path.join(img_dir, 'Laser.png')).convert()
meteor_images = []
listameteor = ['Meteorbig1.png', 'Meteorbig2.png', 'Meteormed1.png', 'Meteormed2.png', 'Meteorsmall1.png', 'Meteorsmall2.png', 'Meteortiny1.png', 'Meteortiny2.png', 'ufoRed.png']
for img in listameteor:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
animacaoexplosao = {}
animacaoexplosao['lg'] = []
animacaoexplosao['sm'] = []
animacaoexplosao['player'] = []
for i in range(9):
    arquivo = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, arquivo)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (60, 60))
    animacaoexplosao['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    animacaoexplosao['sm'].append(img_sm )
    arquivo = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, arquivo)).convert()
    img.set_colorkey(black)
    animacaoexplosao['player'].append(img)
poder_imagens = {}
poder_imagens['shield'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert()
poder_imagens['gun'] = pygame.image.load(path.join(img_dir, 'bolt.png')).convert()

    
#sons
tiro_som = pygame.mixer.Sound(path.join(snd_dir, 'Lasersom2.wav'))
power_som = pygame.mixer.Sound(path.join(snd_dir, 'boltsom1.wav'))
shield_som = pygame.mixer.Sound(path.join(snd_dir, 'shieldsom.wav'))
explosão_sons = []
for snd in ['Explosionsom.wav', 'Explosionsom2.wav']:
    explosão_sons.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))


#musica de fundo
#pygame.mixer.music.load(path.join(snd_dir, ''))
#pygame.mixer.music.set_volume(0.4)
#pygame.mixer.music.play(loops=-1)
#


#Loop do Jogo
game_over = True
running = True
while running:
    if game_over:
        gameover_screen()
        game_over = False
        sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        tiros = pygame.sprite.Group()
        poderes = pygame.sprite.Group()
        player = Player()
        sprites.add(player)
        for i in range(15):
            newenemie()   
        placar = 0
    
    #frames per second 
    clock.tick(fps)
    
    #eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    sprites.update()
    #colisão tiro-inimigo
    hits = pygame.sprite.groupcollide(enemies, tiros, True, True)    
    for hit in hits:
        placar += 56 - hit.radius
        random.choice(explosão_sons).play()
        expl = Explosao(hit.rect.center, 'lg')
        sprites.add(expl)
        if random.random() > 0.96:
            poder = Poder(hit.rect.center)
            sprites.add(poder)
            poderes.add(poder)
        newenemie()
        
    #colisão jogador-inimigo
    hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosao(hit.rect.center, 'sm')
        sprites.add(expl)
        newenemie()
        if player.shield <= 0:
            player_die_sound.play()
            explosao_morte = Explosao(player.rect.center, 'player')
            sprites.add(explosao_morte)
            #player.kill()
           #vidas
            player.hide()
            player.lives -= 1
            player.shield = 100
           #
           
    #colisão jogador-poder
    hits = pygame.sprite.spritecollide(player, poderes, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            #player.shield += 20
            shield_som.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.poder()
            power_som.play()
           
    #Se o jogador morrer e a explosao terminar
    #if not player.alive() and not explosao_morte.alive():
    #vidas
    if player.lives == 0 and not explosao_morte.alive():
    #    
        game_over = True
            
    #Desenho na tela
    screen.fill(black)
    screen.blit(background, background_rect)
    sprites.draw(screen)
    texto_tela(screen, str(placar), 18, width/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    #vidas
    draw_lives(screen, width - 100, 5, player.lives, player_mini_img)
    #
    
    pygame.display.flip()
     
pygame.quit()