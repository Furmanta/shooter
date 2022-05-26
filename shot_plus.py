from pygame import *
from random import randint 
#импорт времени для счетчика, чтобы не спутать
from time import time as timer

mixer.init()
mixer.music.load('Prologue.ogg')
mixer.music.play()
fire_sound = mixer.Sound('mya.ogg')

img_back = "Kosmos.jpg"
img_hero = "cat.png"
img_enemy = "pel.png"
img_bullet = "bul2.png"
#Дополнительные препятствия 
img_ast = 'ch.png'

font.init()
font2 = font.SysFont('Mistral', 36)
font1 = font.SysFont('Mistral', 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))

goal = 10
max_lost = 3
score = 0
lost = 0
#Добавить жизни
life = 3
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost +1
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 30, 40, -15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500

display.set_caption("Битва с пельменями")

window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 80, 10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
#дополнительные препятствия 
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

bullets = sprite.Group()
finish = False
run = True 
#переменная для перезарядки
rel_time = False
#переменная для подсчета выстрелов
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #проверяем, сколько выстрелов сделано и не происходит ли перезарядка
                if num_fire <5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                #если игрок сделал 5 выстрелов
                if num_fire >= 5 and rel_time == False:
                    last_time = timer() #засекаем время, когда произошло
                    rel_time = True #ставим флаг перезарядки
    if not finish:
        window.blit(background, (0,0))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update() #появление препятствий

        ship.reset()
        monsters.draw(window)
        asteroids.draw(window) #отрисовываем при каждой итерации препятствия
        bullets.draw(window)

        #отображаем текст с кол-вом жизни
        text_life = font1.render(str(life), 1, (150, 150,0))
        window.blit(text_life, (650, 10))
        #перезарядка
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('перезарядка...', 1, (150,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, False)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        #добавить астероидов касание и жизни
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids,False):
            sprite.spritecollide(ship, monsters, True)
            sprite. spritecollide(ship, asteroids, True)
            life = life -1
        #проигрыш
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))           
        if score >= goal:
            finish = True
            window.blit(win, (200,200)) 
        text = font2.render('Счёт:    '+ str(score), 1, (255, 255, 255))
        window.blit(text, (10,20))
        text_lose = font2.render('Пропущено:    ' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))   
        display.update()
   #цикл срабатывает каждые 0.05 секунд
    time.delay(50)
