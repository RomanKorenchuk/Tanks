from pygame import *
import numpy
init()

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.start_image = transform.scale(image.load(picture), [w, h])
        self.image = self.start_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        mw.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed, position):
        GameSprite.__init__(self, picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.w = w
        self.h = h
        self.position = position

    def update(self):
        if tank.rect.x <= 1280-100 and tank.x_speed > 0 or tank.rect.x >= 0 and tank.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if tank.rect.y <= 720-90 and tank.y_speed > 0 or tank.rect.y >= 0 and tank.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: 
            for p in platforms_touched:
                self.y_speed = 0              
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire_up(self):
        bullet = Bullet('Bulet_up.png', 4 , 22 , self.rect.right - 25 , self.rect.centery -25, 15, 0)
        bullets.add(bullet)
    def fire_left(self):
        bullet = Bullet("Bulet_left.png", 22 , 4 , self.rect.left , self.rect.centery - 2, 15, 1)
        bullets.add(bullet)
    def fire_right(self):
        bullet = Bullet("Bulet_right.png", 22 , 4 , self.rect.right - 5 , self.rect.centery - 2, 15, 2)
        bullets.add(bullet)
    def fire_back(self):
        bullet = Bullet("Bulet_back.png", 4 , 22 , self.rect.right - 25, self.rect.centery + 15, 15, 3)
        bullets.add(bullet)
    
    def rotate(self):
        self.up_tank = self.start_image
        self.up_rect = self.up_tank.get_rect(center=self.rect.center)
        self.left_tank = transform.rotate(self.start_image, 90)
        self.left_rect = self.left_tank.get_rect(center=self.rect.center)
        self.right_tank = transform.rotate(self.start_image, -90)
        self.right_rect = self.right_tank.get_rect(center=self.rect.center)
        self.back_tank = transform.rotate(self.start_image, 180)
        self.back_rect = self.back_tank.get_rect(center=self.rect.center)
        self.ul_tank = transform.rotate(self.start_image, -45)
        self.ul_rect = self.ul_tank.get_rect(center=self.rect.center)
        self.ur_tank = transform.rotate(self.start_image, 45)
        self.ur_rect = self.ur_tank.get_rect(center=self.rect.center)
        self.bl_tank = transform.rotate(self.start_image, -135)
        self.bl_rect = self.bl_tank.get_rect(center=self.rect.center)
        self.br_tank = transform.rotate(self.start_image, 135)
        self.br_rect = self.br_tank.get_rect(center=self.rect.center)
        self.tanks_i = (self.up_tank, self.left_tank, self.right_tank, self.back_tank, self.ul_tank, self.ur_tank, self.bl_tank, self.br_tank)
        self.tanks_r = (self.up_rect, self.left_rect, self.right_rect, self.back_rect, self.ul_rect, self.ur_rect, self.bl_rect, self.br_rect)
        self.image = self.tanks_i[self.position]
        self.rect = self.tanks_r[self.position]

class Enemy(GameSprite):
    side = 'left'
    def __init__(self, image, w, h, x, y, player_speed,):
        GameSprite.__init__(self,image, w, h, x, y)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 800:
            self.side = 'right'
        if self.rect.x >= 1280 - 150:
            self.side = 'left'

        if self.side == 'left':
            self.rect.x -= self.speed
            self.image = self.start_image
        elif self.side =="right":
            self.rect.x += self.speed
            self.image = transform.rotate(self.start_image, 180)

class Turell(GameSprite):
    def __init__(self, image, w, h, x, y,):
        GameSprite.__init__(self, image, w, h, x, y)
        self.w = w
        self.h = h

    def turell_fire_back(self):
        turell_bullet = Bullet("Bulet_turell_back.png", 4 , 24 , self.rect.right - 30, self.rect.centery + 35, 15, 3)
        turell_bullets.add(turell_bullet)
    
    def turell_fire_left(self):
        turell_bullet = Bullet("Bulet_turell_left.png", 24 , 4 , self.rect.left  , self.rect.centery- 2 , 15, 1)
        turell_bullets.add(turell_bullet)
    
    def turell_fire_back_dvoina(self):
        turell_bullet = Bullet("Bulet_turell_back.png", 4 , 24 , self.rect.right - 40, self.rect.centery + 50, 15, 3)
        turell_bullets.add(turell_bullet)
        turell_bullet = Bullet("Bulet_turell_back.png", 4 , 24 , self.rect.right - 53, self.rect.centery + 50, 15, 3)
        turell_bullets.add(turell_bullet)


class Bullet(GameSprite):
    def __init__(self, image, w, h, x, y, bullet_speed, position):
        GameSprite.__init__(self, image, w, h, x, y)
        self.x_speed = bullet_speed
        self.y_speed = bullet_speed
        self.position = position

    def update(self):
        if self.position == 2:
            self.rect.x += self.x_speed
        elif self.position == 3:
            self.rect.y += self.y_speed
        elif self.position == 1:
            self.rect.x -= self.x_speed
        elif self.position == 0:
            self.rect.y -= self.y_speed 

        if self.rect.x > 1280 + 10 or self.rect.y > 720 + 10:
            self.kill()      

white = (255, 255, 255)
mw = display.set_mode((1280, 720))
mw.fill(white)
display.set_caption(("Tanks"))
picture = image.load("Temnosiri_fon.jpg").convert()
picture = transform.scale(picture, [1280, 720])

barriers = sprite.Group()

bullets = sprite.Group()

turells = sprite.Group()

turell_bullets = sprite.Group()

enemys = sprite.Group()

hedgehogs = sprite.Group()

colide_bullet_1 = GameSprite("Budinok_orange_2.png", 180, 410, 0, 0)
colide_bullet_b_1 = GameSprite("Budinok_orange_2.png", 850, 180, 430, 560)
colide_bullet_b_2 = GameSprite("Budinok_orange_2.png", 850, 180, 430, 560)
colide_bullet_3 = GameSprite("Budinok_orange_2.png", 270, 700, 750, 100)
tank = Player("Pz_4.png", 45, 84, 100, 600, 0, 0, 0)
budinok_orange_1 = GameSprite("Budinok_orange_2.png", 126, 189, 310, 430)
budinok_orange_2 = GameSprite("Budinok_orange_2.png", 126, 189, 310, 575)
budinok_sarai = GameSprite("Budsinok_sarai.png", 150, 150, 0, 400)
polomani_budinki = GameSprite("polamani_budinki_1.png", 187, 112, 155, 140)
podvoeni_1 = GameSprite("Budinok_dlapodvoenia.png", 126, 189, 320, -30)
podvoeni_2 = GameSprite("Budinok_dlapodvoenia.png", 126, 189, 320, 70)
budinok_dvavikna = GameSprite("Budinok_dvavikna.png", 210, 120, 420, 125)
budinok_dvavikna_2 = GameSprite("Budinok_dvavikna.png", 210, 120, 590, 125)
budinok_odnevikno = GameSprite("Budinok_odnevikno.png", 180, 150, 960, 420)
budinok_orange_a = GameSprite("Budinok_orange.png", 189, 126, 520, 430)
budinok_orange_b = GameSprite("Budinok_orange.png", 189, 126, 670, 430)
krugli_budinki = GameSprite("Krugli_budinki.png", 200, 180, 600, 250)
domik_z_balkonom_1 = GameSprite("Domik_z_balkonom_2.png", 180, 150, 1000, 90)
domik_z_balkonom_2 = GameSprite("Domik_z_balkonom.png", 210, 150, 1130, 90)
door = GameSprite("Door.png", 125, 35, 410, 500)
nazhimana_plita = GameSprite("Nazhimna_plita.jpg", 50, 50, 225, 50)

turell = Turell("Turell.png", 60, 85, 50, 0)
big_turell_1 = Turell("B_Turell.png",128, 80, 1100, 640)
big_turell_2 = Turell("B_Turell.png",128, 80, 1100, 555)
turell_dvoina = Turell("Turell_dvoina.png", 90, 110, 850, 50)

maus = Enemy("Maus.png", 150, 60, 1120, 350, 3)
maus_2 = Enemy("Maus.png", 150, 60, 800, 250, 3)

mina = GameSprite("Mina.png", 30, 30, 200, 500)
mina_2 = GameSprite("Mina.png", 30, 30, 900, 500)

hedgehog_1 = GameSprite("Hedgehog.png", 43, 32, 600, 590)
hedgehog_2 = GameSprite("Hedgehog.png", 43, 32, 720, 660)
hedgehog_3 = GameSprite("Hedgehog.png", 43, 32, 840, 590)
hedgehog_4 = GameSprite("Hedgehog.png", 43, 32, 960, 660)
hedgehog_5 = GameSprite("Hedgehog.png", 43, 32, 480, 660)

money = GameSprite("Money.png", 50, 50, 500, 50)

barriers.add(door)
barriers.add(budinok_orange_2)
barriers.add(budinok_orange_1)
barriers.add(budinok_sarai)
barriers.add(podvoeni_1)
barriers.add(podvoeni_2)
barriers.add(budinok_dvavikna)
barriers.add(budinok_dvavikna_2)
barriers.add(budinok_odnevikno)
barriers.add(polomani_budinki)
barriers.add(budinok_orange_a)
barriers.add(budinok_orange_b)
barriers.add(krugli_budinki)
barriers.add(domik_z_balkonom_2)
barriers.add(domik_z_balkonom_1)
enemys.add(maus)
enemys.add(maus_2)
enemys.add(mina)
enemys.add(mina_2)
enemys.add(hedgehog_1)
enemys.add(hedgehog_2)
enemys.add(hedgehog_3)
enemys.add(hedgehog_4)
enemys.add(hedgehog_5)
hedgehogs.add(hedgehog_1)
hedgehogs.add(hedgehog_2)
hedgehogs.add(hedgehog_3)
hedgehogs.add(hedgehog_4)
hedgehogs.add(hedgehog_5)
turells.add(turell)
turells.add(big_turell_1)
turells.add(big_turell_2)
turells.add(turell_dvoina)

bulletsamount_t = 20
reloading_t = 0
bulletsamount_1_bt = 1
reloading_1_bt = 0
bulletsamount_2_bt = 1
reloading_2_bt = 0
bulletsamount_td = 30
reloading_td = 0

clock = time.Clock()
    
run = True
finish = False
t_i = True
cb_1_i = True
t_b_1_i = True
t_b_2_i = True
cbb_1_i = True
cbb_2_i = True
t_d_i = True
cb_3_i = True

while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            '''if e.key == K_w and e.key == K_a:
                tank.x_speed = -4
                tank.y_speed = -4
                tank.position = 4
            elif e.key == K_w and e.key == K_d:
                tank.x_speed = 4
                tank.y_speed = -4
                tank.position = 5
            elif e.key == K_s and e.key == K_a:
                tank.x_speed = -4
                tank.y_speed = 4
                tank.position = 6
            elif e.key == K_s and e.key == K_d:
                tank.x_speed = 4
                tank.y_speed = 4
                tank.position = 7'''
            if e.key == K_a:
                tank.x_speed = -10
                tank.position = 1     
            elif e.key == K_d:
                tank.x_speed = 10
                tank.position = 2
            elif e.key == K_w :
                tank.y_speed = -10
                tank.position = 0
            elif e.key == K_s :
                tank.y_speed = 10
                tank.position = 3
            elif e.key == K_SPACE and tank.position == 1:
                tank.fire_left()
            elif e.key == K_SPACE and tank.position == 2:
                tank.fire_right()
            elif e.key == K_SPACE and tank.position == 0:
                tank.fire_up()
            elif e.key == K_SPACE and tank.position == 3:
                tank.fire_back()
 
        elif e.type == KEYUP:
            if e.key == K_a :
                tank.x_speed = 0
            elif e.key == K_d:
                tank.x_speed = 0
            elif e.key == K_w:
                tank.y_speed = 0
            elif e.key == K_s:
                tank.y_speed = 0  

    if not finish:
        if bulletsamount_t == 0:
            reloading_t += 1
            if reloading_t >= 35:
                bulletsamount_t += 20
                reloading_t = 0
        if bulletsamount_1_bt == 0:
            reloading_1_bt +=1
            if reloading_1_bt >= 15:
                bulletsamount_1_bt += 1
                reloading_1_bt = 0
        if bulletsamount_2_bt == 0:
            reloading_2_bt += 1
            if reloading_2_bt >= 15:
                bulletsamount_2_bt += 1
                reloading_2_bt = 0
        if bulletsamount_td == 0:
            reloading_td += 1
            if reloading_td >= 35:
                bulletsamount_td += 30
                reloading_td = 0

        colide_bullet_1.reset()
        colide_bullet_b_1.reset()
        colide_bullet_b_2.reset()
        colide_bullet_3.reset()
        mw.blit(picture, [0, 0])
        barriers.draw(mw)

        enemys.draw(mw)
        enemys.update()

        money.reset()
        nazhimana_plita.reset()

        turell_bullets.draw(mw)
        turell_bullets.update()
        bullets.draw(mw)
        bullets.update()
        if t_b_1_i:
            big_turell_1.reset()
        if t_b_2_i:
            big_turell_2.reset()
        if t_d_i:
            turell_dvoina.reset()
        if t_i:
            turell.reset()

        tank.reset()
        tank.update() 
        tank.rotate()

    sprite.groupcollide(bullets, hedgehogs, True, True)
    sprite.groupcollide(bullets, barriers, True, False)
    sprite.groupcollide(turell_bullets, barriers, True, False)
    sprite.groupcollide(bullets, enemys, True, False)

    if sprite.collide_rect(tank, colide_bullet_1) and cb_1_i and bulletsamount_t > 0:
        bulletsamount_t -=1
        turell.turell_fire_back()
        turell.kill()
    if sprite.collide_rect(tank, colide_bullet_b_1) and cbb_1_i and bulletsamount_1_bt > 0:
        bulletsamount_1_bt -=1
        big_turell_1.turell_fire_left()
    if sprite.collide_rect(tank, colide_bullet_b_1) and cbb_2_i and bulletsamount_2_bt > 0:
        bulletsamount_2_bt -=1
        big_turell_2.turell_fire_left()
    if sprite.collide_rect(tank, colide_bullet_3) and cb_3_i and bulletsamount_td > 0:
        bulletsamount_td -=1
        turell_dvoina.turell_fire_back_dvoina()

    if sprite.collide_rect(tank, nazhimana_plita):
        door.kill()
    if sprite.spritecollide(turell, bullets, True) or sprite.collide_rect(tank, turell):
        t_i = False
        cb_1_i = False
    if sprite.spritecollide(big_turell_1, bullets, True) or sprite.collide_rect(tank, big_turell_1):
        t_b_1_i = False
        cbb_1_i = False
    if sprite.spritecollide(big_turell_2, bullets, True) or sprite.collide_rect(tank, big_turell_2):
        t_b_2_i = False
        cbb_2_i = False
    if sprite.spritecollide(turell_dvoina, bullets, True) or sprite.collide_rect(tank, turell_dvoina):
        t_d_i = False
        cb_3_i = False

    kill = sprite.spritecollide(tank, turell_bullets, True)
    kill2 = sprite.spritecollide(tank, enemys, False)
    #kill3 = sprite.collide_rect(tank, big_turell_1) or sprite.collide_rect(tank, big_turell_2) or sprite.collide_rect(tank, turell_dvoina)
    if kill or kill2:
        finish = True
        lose = transform.scale(image.load("Lose.jpg"), [1280, 720])
        mw.fill((255, 255, 255))
        mw.blit(lose, (0, 0))

    if sprite.collide_rect(tank, money):
        finish = True
        win = transform.scale(image.load("Win.jpg"), [1280, 720])
        mw.fill((255, 255, 255))
        mw.blit(win, (0, 0))

    display.update()
    clock.tick(40)

    

