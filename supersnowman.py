

import pygame

# Визначення кількості кольорів 
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
lightblue = (204,255,255)
brown = (153,76,0)
green = (0,255,0)
darkbrown = (100,50,0)

icon=pygame.image.load('images/supersnowman.png')
pygame.display.set_icon(icon)

# Додавання музики
pygame.mixer.init()
pygame.mixer.music.load('letitsnow.mp3')
pygame.mixer.music.play(-1, 0.0)

# Цей клас представляє платформу, на яку стрибають
class Platform (pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()

class Flake_Platform (pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.image.load(filename).convert_alpha()
        
        # Зробить верхній лівий кут місцем передачі
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y
        self.hasflake = True

class Transparent (pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.Surface([width, height])
        self.image.set_alpha(0)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        screen.blit(self.image, (0,0))

class ImgPlatform (pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.image.load(filename).convert_alpha()
        
        # Зробить верхній лівий кут місцем передачі
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

# Цей клас представляє Super Snowman, яким гравець керує 
class Player(pygame.sprite.Sprite):
   
    # -- Атрибути 
    # Встановити вектор швидкості гравця
    change_x=0
    change_y=0
 
    # Спрацьовує, якщо гравець хоче стрибнути
    jump_ready = False
 
    # Підрахунок кадрів з моменту, коли гравець натиснув «стрибок» і
    # зіткнувся з чимось. Використовується для запобігання стрибків
    # коли ні в що не влучили
    frame_since_collision = 0
    frame_since_jump = 0
     
    # -- Методи 
    # Функція конструктора 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
 
        # Список, до якого будуть збережені зображення
        self.images=[]
        # Завантажити зображення 1 і 2
        for i in range(1,3):
            img = pygame.image.load("images/pingu"+str(i)+".png").convert_alpha()
            img.set_colorkey(white)
            self.images.append(img)
         
        # За замовчуванням використовуйте зображення 0
        self.image = self.images[0]
        
        # Зробить верхній лівий кут місцем передачі
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y
       
    # Змінити швидкість програвача 
    def changespeed_x(self,x):
        self.change_x = x
 
    def changespeed_y(self,y):
        self.change_y = y

    # Знаходить нову позицію для гравця 
    def update(self,blocks,flake_blocks,flakes): 
 
        # Збереже стару позицію x, оновить і подивитьмя, чи не зіткнулися нізчим.
        old_x = self.rect.x
        new_x = old_x + self.change_x
        self.rect.x = new_x

        if self.change_x < 0:
            self.image = self.images[1]
        elif self.change_x > 0:
            self.image = self.images[0]
 
        collide = pygame.sprite.spritecollide (self, blocks, False)
        if collide:
            # Зіткнулися, повернеться на старе місце до зіткнення
            self.rect.x = old_x

        fbcollide = pygame.sprite.spritecollide(self, flake_blocks, False)
        if fbcollide:
            self.rect.x = old_x

        # Збереже стару позицію y, оновить і подивитьмя, чи не зіткнулися нізчим.
        old_y = self.rect.y 
        new_y = old_y + self.change_y 
        self.rect.y = new_y

        if new_y > 600:
            gameOver("lost")

        for fbcollide in pygame.sprite.spritecollide (self, flake_blocks, False):
            # if fbcollide:
            # Зіткнулися, повернеться на старе місце до зіткнення
            self.rect.y = old_y
            self.rect.x = old_x
            # Зупинить наш вертикальний рух
            self.change_y = 0
 
            # Починає рахувати кадри з того моменту, як ми щось зачепили
            self.frame_since_collision = 0

            if fbcollide.hasflake == True and self.frame_since_jump < 115 and self.frame_since_jump > 101:
                flake = ImgPlatform(16, 16, "images/helves.png")
                # Встановити x та y 
                flake.rect.x = fbcollide.rect.x+2
                flake.rect.y = fbcollide.rect.y-20
                fbcollide.hasflake = False
         
                flake_list.add(flake)
                all_sprites_list.add(flake)
         
        block_hit_list = pygame.sprite.spritecollide(self, blocks, False)
 
        for block in block_hit_list:
            # Зіткнулися. Встановити старе місце до зіткнення
            self.rect.y = old_y
            self.rect.x = old_x
 
            # Зупинить вертикальний рух
            self.change_y = 0
 
            # Починає рахувати кадри з того моменту, як щось зачепили
            self.frame_since_collision = 0
 
        # Якщо гравець нещодавно попросив стрибнути, 
        # а у нас нещодавно була земля під ногами, 
        # змініть швидкість, щоб відправити нас вгору
        if self.frame_since_collision < 10 and self.frame_since_jump < 10:
            self.frame_since_jump = 100
            self.change_y -= 11
 
        # Збільшення лічильників кадрів
        self.frame_since_collision+=1
        self.frame_since_jump+=1
 
    # Обчислити дію сили тяжіння
    def calc_grav(self):
        self.change_y += .35
 
        # Перевірте, чи на землі
        if self.rect.y >= 600 and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = 600
            self.frame_since_collision = 0
 
    # Викликається, коли користувач натискає кнопку "Перейти"
    def jump(self,blocks):
        self.jump_ready = True
        self.frame_since_jump = 0

class FireCreature(Player):
    def __init__(self,x,y): 
        pygame.sprite.Sprite.__init__(self)
        # Список, до якого будуть збережені зображення.
        self.images=[]
        # Завантажити зображення 1 і 2
        for i in range(1,3):
            img = pygame.image.load("images/leek"+str(i)+".png").convert_alpha()
            img.set_colorkey(white)
            self.images.append(img)
         
        # За замовчуванням використовуйте зображення 0
        self.image = self.images[0]
        
        # Зробіть наш верхній лівий кут місцем передачі.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y
        self.direction = "left"

    def changespeed(self,x1,x2):
        if self.rect.x <= x2:
            self.direction = "right"
        elif self.rect.x >= x1:
            self.direction = "left"

    def update(self,diff):
        if self.direction == "left":
            self.change_x = -3
        elif self.direction == "right":
            self.change_x = 3
        else:
            self.change_x = -3

        # Збережіть стару позицію x, поновіть і подивіться, чи не зіткнулися ми.
        old_x = self.rect.x - diff
        new_x = old_x + self.change_x
        self.rect.x = new_x

        if new_x % 2 == 0:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        
pygame.init()

# Налаштуйте висоту та ширину екрана 
size=[800,600]
screen=pygame.display.set_mode(size)

pygame.display.set_caption("Super Snowman")

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

# Створюйте платформи
def create_level1(block_list,flake_list,all_sprites_list):

    ground = {0:1390,1460:500,2400:200,2700:100,2900:100,3100:600,3850:800,5000:150,
              5250:750}
    for x in ground:
        block = Transparent(white, ground[x], 80)
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 520

        block_list.add(block)
        all_sprites_list.add(block)

    #Нижні блоки
    lst1 = [500,800,1000,1040,1080,1120,1160,
            1200,1240,2000,2020,2220,2240,4000,4020,4170,4190,
            4210,4250,4290,4300,4320,4725,4855,4965]
    for x in lst1:
        block = ImgPlatform(20, 20, "images/alus.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 360
 
        block_list.add(block)
        all_sprites_list.add(block)

    #Верхні блоки
    lst2 = [200,300,600,620,680,700,1020,1130,1240,2100,2120,
            2340,2360,4075,4095,4115,4800,4910]
    for x in lst2:
        block = ImgPlatform(20, 20, "images/alus.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 200
 
        block_list.add(block)
        all_sprites_list.add(block)

    #Блоки точок скління
    lst13=[1075,1185]
    for x in lst13:
        block = Flake_Platform(20, 20, "images/kast.png")
        # Встановити x та y
        block.rect.x = x
        block.rect.y = 200
        block.hasflake = True
 
        flake_block_list.add(block)
        all_sprites_list.add(block)

    #Блоки нижньої точки
    lst12=[150,650,1020,1060,1100,1140,1180,1220,1260,4230,4270]
    for x in lst12:
        block = Flake_Platform(20, 20, "images/kast.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 360
        block.hasflake = True
 
        flake_block_list.add(block)
        all_sprites_list.add(block)
    

    #Вертикальні труби
    lst3 = [3580,3940,5420]
    for x in lst3:
        block = ImgPlatform(30, 20, "images/kand20.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 500
 
        block_list.add(block)
        all_sprites_list.add(block)

    lst4 = [3610,3910,5450]
    for x in lst4:
        block = ImgPlatform(30, 40, "images/kand40.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 480
 
        block_list.add(block)
        all_sprites_list.add(block)


    lst5 = [400,900,1360,1460,3250,3640,3880,4620,5480]
    for x in lst5:
        block = ImgPlatform(30, 60, "images/kand60.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 460
 
        block_list.add(block)
        all_sprites_list.add(block)

    lst6 = [3670,3850,5510]
    for x in lst6:
        block = ImgPlatform(30, 80, "images/kand80.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 440
 
        block_list.add(block)
        all_sprites_list.add(block)

    lst7 = [5540]
    for x in lst7:
        block = ImgPlatform(30, 100, "images/kand100.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 420
 
        block_list.add(block)
        all_sprites_list.add(block)

    lst8 = [5570]
    for x in lst8:
        block = ImgPlatform(30, 120, "images/kand120.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 400
 
        block_list.add(block)
        all_sprites_list.add(block)

    lst9 = [5600]
    for x in lst9:
        block = ImgPlatform(30, 140, "images/kand140.png")
        # Встановити x та y 
        block.rect.x = x
        block.rect.y = 380
        
        block_list.add(block)
        all_sprites_list.add(block)


    edge1 = Transparent(white, 100, 600)
    # Встановити x та y 
    edge1.rect.x = 0
    edge1.rect.y = 0

    block_list.add(edge1)
    all_sprites_list.add(edge1)

    edge2 = Transparent(white, 100, 600)
    # Встановити x та y  
    edge2.rect.x = 5900
    edge2.rect.y = 0

    block_list.add(edge2)
    all_sprites_list.add(edge2)



# Основна програма, створення блоків
block_list = pygame.sprite.RenderPlain()

flake_list = pygame.sprite.RenderPlain()

flake_block_list = pygame.sprite.RenderPlain()

fire_creatures = pygame.sprite.RenderPlain()

endpoint = pygame.sprite.RenderPlain()

all_sprites_list = pygame.sprite.RenderPlain()

player_list = pygame.sprite.RenderPlain()

create_level1(block_list,flake_list,all_sprites_list)

background = pygame.image.load("images/taust.png").convert()

bgr = Platform(0,0,0)

castle = ImgPlatform(200, 200, "images/loss.png")
# Встановити x та y
castle.rect.x = 5765
castle.rect.y = 320
all_sprites_list.add(castle)


last_block = Transparent(white, 100, 40)
# Встановити x та y
last_block.rect.x = 5890
last_block.rect.y = 480
endpoint.add(last_block)
all_sprites_list.add(last_block)

# Використовується для керування швидкістю оновлення екрана 
clock=pygame.time.Clock()

# -------- Основний цикл програми ----------- 
def startGame():

    player = Player(20, 40)

    player.rect.x = 100
    player.rect.y = 485

    player_list.add(player)


    fire1 = FireCreature(20,37)
    fire1.rect.x = 380
    fire1.rect.y = 483
    all_sprites_list.add(fire1)
    fire_creatures.add(fire1)

    fire2 = FireCreature(20,37)
    fire2.rect.x = 880
    fire2.rect.y = 483
    all_sprites_list.add(fire2)
    fire_creatures.add(fire2)

    fire3 = FireCreature(20,37)
    fire3.rect.x = 1320
    fire3.rect.y = 483
    all_sprites_list.add(fire3)
    fire_creatures.add(fire3)

    fire4 = FireCreature(20,37)
    fire4.rect.x = 1960
    fire4.rect.y = 483
    all_sprites_list.add(fire4)
    fire_creatures.add(fire4)

    fire5 = FireCreature(20,37)
    fire5.rect.x = 3500
    fire5.rect.y = 483
    all_sprites_list.add(fire5)
    fire_creatures.add(fire5)

    fire6 = FireCreature(20,37)
    fire6.rect.x = 4600
    fire6.rect.y = 483
    all_sprites_list.add(fire6)
    fire_creatures.add(fire6)

    fire7 = FireCreature(20,37)
    fire7.rect.x = 1240
    fire7.rect.y = 320
    all_sprites_list.add(fire7)
    fire_creatures.add(fire7)


    #Зациклюється, поки користувач не натисне кнопку закриття 
    done=False

    score = 0

    while done==False:

        for event in pygame.event.get(): # Користувач зробив щось
            if event.type == pygame.QUIT: # Якщо користувач натиснув закрити
                done=True # Позначте, що ми закінчили, щоб вийти з цього циклу
     
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed_x(-6)
                if event.key == pygame.K_RIGHT:
                    player.changespeed_x(6)
                if event.key == pygame.K_UP:
                    player.jump(block_list)
                if event.key == pygame.K_DOWN:
                    player.changespeed_y(6)
                     
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed_x(-0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed_x(0)

        # Обертайте плеєр навколо екрана, якщо він занадто далеко відходить вліво/вправо
        if player.rect.x >= 700:
            diff = player.rect.x - 700
            diff2 = player.rect.x - 700
            player.rect.x=700
            for block in block_list:
                block.rect.x -= diff
            for flake in flake_list:
                flake.rect.x -= diff
            for f_block in flake_block_list:
                f_block.rect.x -= diff
            bgr.rect.x -= diff
            bgr.rect.y = 0
            castle.rect.x -= diff
            last_block.rect.x -= diff
        elif player.rect.x <= 100:
            diff = 100 - player.rect.x
            diff2 = player.rect.x - 100
            player.rect.x=100
            for block in block_list:
                block.rect.x += diff
            for flake in flake_list:
                flake.rect.x += diff
            for f_block in flake_block_list:
                f_block.rect.x += diff
            bgr.rect.x += diff
            bgr.rect.y = 0
            castle.rect.x += diff
            last_block.rect.x += diff

        bgpos = bgr.rect.x

        player.calc_grav()
        player.update(block_list,flake_block_list,flake_list)
        
        fire1.changespeed(380+bgpos,100+bgpos)
        fire1.update(diff2)

        fire2.changespeed(880+bgpos,500+bgpos)
        fire2.update(diff2)

        fire3.changespeed(1320+bgpos,960+bgpos)
        fire3.update(diff2)

        fire4.changespeed(1960+bgpos,1490+bgpos)
        fire4.update(diff2)

        fire5.changespeed(3500+bgpos,3280+bgpos)
        fire5.update(diff2)

        fire6.changespeed(4600+bgpos,3970+bgpos)
        fire6.update(diff2)

        fire7.changespeed(1240+bgpos,1000+bgpos)
        fire7.update(diff2)


        flakes_hit_list = pygame.sprite.spritecollide(player, flake_list, True)

        if len(flakes_hit_list) > 0:
            score +=len(flakes_hit_list)

        # Налаштування фону екрана
        if bgr.rect.x <= 0 and bgr.rect.x >= -5200:
            screen.blit(background, bgr)
            block_list.update()
            flake_list.update()
            flake_block_list.update()
        elif bgr.rect.x > 0:
            bgr.rect.x = 0
            screen.blit(background, bgr)
        elif bgr.rect.x < -5200:
            bgr.rect.x = -5200
            screen.blit(background, bgr)

        text=font.render("Score: "+str(score), True, red)
        screen.blit(text, [10, 10])
        
        # ВЕСЬ КОД ДЛЯ МАЛЮВАННЯ ПОВИНЕН БУТИ НИЖЧЕ ЦЬОГО КОМЕНТАРЯ 
        all_sprites_list.draw(screen)
        player_list.draw(screen)
        # ВЕСЬ КОД ДЛЯ МАЛЮВАННЯ ПОВИНЕН БУТИ ВИЩЕ ЦЬОГО КОМЕНТАРЯ 
        
        fire_hit = pygame.sprite.spritecollide(player, fire_creatures, False)

        if fire_hit:
            done = True
            gameOver("lost")

        last_hit = pygame.sprite.spritecollide(player, endpoint, False)
        if last_hit:
            done = True
            gameOver("won")


        # Оновлюємо екран тим, що ми намалювали. 
        pygame.display.flip()
        
        # Обмеження до 30 кадрів на секунду 
        clock.tick(30)


def gameOver(state):
    done = False
    while done==False:
        for event in pygame.event.get(): # Користувач зробив щось 
            if event.type == pygame.QUIT: # Якщо користувач натиснув закрити 
                done=True # Позначити, що закінчили, щоб вийти з цього циклу
        if state == "lost":
            text=font.render("Game over", True, red)
            screen.blit(text, [340, 300])
        elif state == "won":
            text=font.render("You  won!", True, red)
            screen.blit(text, [350, 300])

        # Оновлення екрану тим, що намальовано. 
        pygame.display.flip()

        # Обмеження до 30 кадрів на секунду 
        clock.tick(30)
    
startGame()

pygame.quit ()