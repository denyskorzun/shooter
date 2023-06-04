from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_x, player_y, width, height, player_image=None, bg_color="green"):
        super().__init__()
        if player_image:
            self.image = transform.scale(image.load(player_image), (width, height))    
        else:
            self.image = Surface((width, height))
            self.image.fill(bg_color)

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_x, player_y, 65, 65, player_image)
        self.speed = player_speed
        self.sprite_flip = "r"

    def move(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 0:
            if self.sprite_flip == "r":
                self.image = transform.flip(self.image, True, False)
                self.sprite_flip = "l"
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            if self.sprite_flip == "l":
                self.image = transform.flip(self.image, True, False)
                self.sprite_flip = "r"
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 435:
            self.rect.y += self.speed

class Cyborg(GameSprite):
    def __init__(self, player_image, player_start_x, player_end_x, player_y, player_speed):
        super().__init__(player_start_x, player_y, 65, 65, player_image)
        self.speed = player_speed
        self.player_start_x = player_start_x
        self.player_end_x = player_end_x
        if player_speed > 0:
            self.sprite_flip = "r"
        else:
            self.sprite_flip = "l"
            self.image = transform.flip(self.image, True, False)



    def move(self):

        self.rect.x += self.speed
        if self.rect.x >= self.player_end_x or self.rect.x <= self.player_start_x:
            self.speed *= -1

            self.image = transform.flip(self.image, True, False)


        # if self.sprite_flip == "l":
        #     self.image = transform.flip(self.image, True, False)
        #     self.sprite_flip = "r"

        # keys_pressed = key.get_pressed()

        # if keys_pressed[K_a] and self.rect.x > 0:
        #     self.rect.x -= self.speed
        # if keys_pressed[K_d] and self.rect.x < 635:
        #     self.rect.x += self.speed
        # if keys_pressed[K_w] and self.rect.y > 0:
        #     self.rect.y -= self.speed
        # if keys_pressed[K_s] and self.rect.y < 435:
        #     self.rect.y += self.speed



class Wall(GameSprite):
    def __init__(self, player_x, player_y, bg_color, width, height):
        super().__init__(player_x, player_y, width, height, None, bg_color)
        self.width = width
        self.height = height


mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
custom_font = font.Font(None, 70)
win = custom_font.render('YOU WIN!', True, (255, 215, 0))
lose = custom_font.render('YOU LOSE!', True, (180, 0, 0))

window = display.set_mode((700, 500))
display.set_caption("Доганялки")
background = transform.scale(image.load("background.jpg"), (700, 500))

# дані про спрайт-картинку

hero = Hero('hero.png', 0, 50, 3)
cyborg = Cyborg('cyborg.png', 200, 500, 100, 5)
cyborg1 = Cyborg('cyborg.png', 300, 600, 300, 5)
gold = GameSprite(594, 420, 106, 80, 'treasure.png')

walls = [
    Wall(100, 20, "green", 560, 5),
    Wall(100, 20, "green", 5, 400),
    Wall(200, 100, "green", 5, 400),
    Wall(200, 100, "green", 100, 5),
    Wall(300, 100, "green", 5, 220),
    Wall(300, 320, "green", 180, 5),
    Wall(380, 100, "green", 5, 140),
    Wall(380, 100, "green", 180, 5),
    Wall(560, 100, "green", 5, 320),
    Wall(660, 20, "green", 5, 400),
    Wall(610, 100, "yellow", 5, 140),
    Wall(475, 240, "red", 5, 80),
    Wall(380, 420, "green", 185, 5),

]


# ігровий цикл
run = True
game_over = False
is_win = False
clock = time.Clock()
FPS = 60

while run:
    window.blit(background,(0, 0))
    hero.reset()
    cyborg.reset()
    cyborg1.reset()
    gold.reset()

    for w in walls:
        w.reset()

    for e in event.get():
        if e.type == QUIT:
            run = False
    
    if not game_over:
        hero.move(); draw.rect(window, (255, 0, 0), hero.rect, 2)
        cyborg.move()
        cyborg1.move()
        
        for w in walls:
            if sprite.collide_rect(hero, w):
                game_over = True
                kick.play()
                
    

        if sprite.collide_rect(hero, gold):
            money.play()
            game_over = True
            is_win = True

        if sprite.collide_rect(hero, cyborg):
            game_over = True
            kick.play()
        if sprite.collide_rect(hero, cyborg1):
            game_over = True
            kick.play()
    

    else:
        if is_win == True:
            window.blit(win, (200, 200))
        else:
            window.blit(lose, (200, 200))


    display.update()
    clock.tick(FPS)
