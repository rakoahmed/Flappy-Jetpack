# Importing libraries
import pygame
import random
import os


# Initialize fonts in pygame
pygame.font.init()

# Initialize the game engine
pygame.init()

# Setting the width and height of the screen
width, height = 800, 750
screen = pygame.display.set_mode((width, height))

# Setting the caption of the window
pygame.display.set_caption("Galaxy Wars")

# ------- Loading all the images to be used as sprites. -------
# I thought it's nicer to use images instead of random shapes

# Main charater player
MAIN_CHARACTER = pygame.image.load(os.path.join("assets", "main_character.png"))

# Enemy character players
ENEMY_1 = pygame.image.load(os.path.join("assets", "enemy_1.png"))
ENEMY_2 = pygame.image.load(os.path.join("assets", "enemy_2.png"))
ENEMY_3 = pygame.image.load(os.path.join("assets", "enemy_3.png"))

# ------- Loading bullet images -------
# Main character Laser bullet
MAIN_CHARACTER_BULLET = pygame.image.load(os.path.join("assets", "main_character_bullet.png"))

# Enemy characters laser bullets
ENEMY_BULLET_1 = pygame.image.load(os.path.join("assets", "enemy_1_bullet.png"))
ENEMY_BULLET_2 = pygame.image.load(os.path.join("assets", "enemy_2_bullet.png"))
ENEMY_BULLET_3 = pygame.image.load(os.path.join("assets", "enemy_3_bullet.png")) 

# Game background
# --- I use 'pygame.transform.scale' method to scale the background image so it can fill the entire screen ---
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "galaxy_bg.png")), (width, height))

""" --- Musics & Sound Affects --- """
# main theme music
music = pygame.mixer.music.load('theme_music.mp3')

# laser shots sound
laser_sound = pygame.mixer.Sound('laser_sound.wav')

# game over sound
game_over = pygame.mixer.Sound('game_over.wav')

# collision sound between the player and enemy ship.
collide_sound = pygame.mixer.Sound('collide_sound.wav')

# setting the main theme music to -1, so it can replay the music after it's finished
pygame.mixer.music.play(-1)

# -----------------------------------------

# Creating a general class which can hold general attributes for all ship 
# some of its properties are for both player and enemy ship: 
# ----- PARENT CLASS -----
class Bullet():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        return not(self.y < height and self.y >= 0)
    
    def collision(self, object):
        return collide(self, object)


class Ship():
    # making a class variable to set the cooldown to 30 FPS (half-second) becasue the main FPS is 60
    COOLDOWN = 30

    """Creating an __init__ method which can store our ship's properties in the game"""
    def __init__(self, x, y, hearts=100):
        self.x = x
        self.y = y
        self.hearts = hearts
        self.ship_img = None
        self.bullet_img = None
        self.bullets = []
        self.cool_down_counter = 0
    
    # defining a method to draw the ship on the screen
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window) 
    
    # moving the bullets, removing the bullets from their list when they
    # go off the screen, and losing %10 hearts when colliding with a bullet
    def move_bullets(self, velocity, object):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(velocity)
            if bullet.off_screen(height):
                self.bullets.remove(bullet)
            elif bullet.collision(object):
                object.hearts -= 10
                self.bullets.remove(bullet)

    # Defining a method to handle counting the cooldown track,
    # this if statement states that if this cooldown counter is zero,
    # don't do anything. If, however, is gretaer than 0, then increment the cooldown counter by 1.
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Define a method that will shoot the bullets
    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    # defining a function so the ship doesn't exit the WIDTH
    def get_width(self):
        return self.ship_img.get_width()

    # defining a function so the ship doesn't exit the HEIGHT
    def get_height(self):
        return self.ship_img.get_height()

# main character's inheritance from Ship, parent class
class Player(Ship):
    def __init__(self, x, y, hearts=100):
        super().__init__(x, y, hearts)
        self.ship_img = MAIN_CHARACTER
        self.bullet_img = MAIN_CHARACTER_BULLET
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_hearts = hearts
    
    def move_bullets(self, velocity, objects):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(velocity)
            if bullet.off_screen(height):
                self.bullets.remove(bullet)
            else:
                for object in objects: 
                    if bullet.collision(object):
                        objects.remove(object)
                        self.bullets.remove(bullet)

    def draw(self, window):
        super().draw(window)
        self.heartbar(window)
    
    def heartbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.hearts/self.max_hearts), 10))

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x + 40, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

# enemy's inheritance from Ship, parent class
class Enemy(Ship):
    colorMap = {
        "enemy_1":(ENEMY_1, ENEMY_BULLET_1),
        "enemy_2":(ENEMY_2, ENEMY_BULLET_2),
        "enemy_3":(ENEMY_3, ENEMY_BULLET_3)
    }

    def __init__(self, x, y, color, hearts=100):
        super().__init__(x, y, hearts)
        self.ship_img, self.bullet_img = self.colorMap[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity

    
    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x + 25, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None 

# making a list to store random stars in.
star_list = []

# making a for loop to generate 100 random stars for each wave.
for stars in range(200):
    x = random.randrange(0, 800)
    y = random.randrange(0, 750)
    star_list.append([x, y])

""" DEFINING A FUNCTION THE REPRESENTS THE MAIN LOOP PROGRAM! """
def main_loop():
    run = True
    FPS = 60
    level = 0
    hearts = 5
    game_font = pygame.font.SysFont("comicsans", 25)
    lost_font = pygame.font.SysFont("arial", 50)
    
    # This list stores where all the enemies are
    enemies = []
    wave_length = 5
    enemy_velocity = 1

    # Player and bullet's velocity
    player_velocity = 5
    bullet_velocity = 6

    # creating an instance of Player class
    player = Player(300, 630)

    # setting up the clock
    clock = pygame.time.Clock()

    # checking if the game is over
    lost = False

    # setting a variable to track the lost counts
    lost_count = 0
    
    def redraw_screen():
        # drawing the BACKGROUND 
        screen.blit(BG, (0,0))

        # making a for loop to generate random stars in random locations.
        for star in star_list:
            star[1] += 1
            pygame.draw.circle(screen, (255,255,255), star, 2)
            if star[1] > 750:
                star[1] = random.randrange(-20, -5)
                star[0] = random.randrange(800)
                
        # drawing FONTS on the screen
        hearts_label = game_font.render(f"Hearts: {hearts}", 1, (255,255,255))
        level_label = game_font.render(f"Level: {level}", 1, (255,255,255))

        # drawing the LEVEL and HEARTS on the screen
        screen.blit(hearts_label, (10,10))
        screen.blit(level_label, (width - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(screen)

        # drawing the PLAYER on the screen
        player.draw(screen)

        # displaying the 'GAME OVER!' text on the screen if we lose
        if lost:
            lost_label = lost_font.render("GAME OVER!", 1, (255,255,255))
            screen.blit(lost_label,(width/2 - lost_label.get_width()/2, 350))
        
        # finally updating the screen with what we've drawn
        pygame.display.update()


    while run:
        # setting the FPS with the clock
        clock.tick(FPS)
        redraw_screen()

        # check to see of the hearts is less than 0, then lose.
        if hearts <= 0 or player.hearts <= 0:
            lost = True
            lost_count += 1       

        # if the game is lost, and the user is on the screen for more than 3 seconds,
        # then quit the game, or go back to main menu; otherwise, continue.
        if lost:
            if lost_count > FPS * 3:
                game_over.play()
                run = False
            else:
                continue
        
        # for each enemy wave, get the enemies started on a random location offset the y position.
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range (wave_length):
                enemy = Enemy(random.randrange(50, width - 100), random.randrange(-1500, -100,), random.choice(["enemy_1", "enemy_2", "enemy_3"]))
                enemies.append(enemy)

        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT


        # GAME LOGIC SHOULD GO BELOW THIS COMMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0: # Press a to move LEFT
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < width: # press d to move RIGHT
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0: # press w to move UP
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() + 20 < height: # press s to move DOWN
            player.y += player_velocity

        # check to see if left-click pressed, the shoot a bullet object
        if keys[pygame.K_SPACE]:
            player.shoot()
            laser_sound.play()

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_bullets(bullet_velocity, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                collide_sound.play()
                player.hearts -= 10
                enemies.remove(enemy)
            
            elif enemy.y + enemy.get_height() > height:
                hearts -= 1
                enemies.remove(enemy)

        player.move_bullets(-bullet_velocity, enemies)

        # GAME LOGIC SHOULD GO ABOVE THIS COMMENT

def main_menu():
    title_font = pygame.font.SysFont("Arial", 50)
    run = True
    while run:
        # show the background first 
        screen.blit(BG, (0,0))

        # Press the mouse to begin
        title_label = title_font.render("Press the MOUSE to begin...", 1, (255,255,255), 1)    
        screen.blit(title_label, (width/2 - title_label.get_width()/2, 200))

        # Press W to move Up
        title_label = title_font.render("Press W to move FORWARD", 1, (255,255,255))    
        screen.blit(title_label, (width/2 - title_label.get_width()/2, 300))

        # Press D to move RIGHT
        title_label = title_font.render("Press D to move RIGHT", 1, (255,255,255))    
        screen.blit(title_label, (width/2 - title_label.get_width()/2, 350))

        # Press A to move LEFT
        title_label = title_font.render("Press A to move LEFT", 1, (255,255,255))    
        screen.blit(title_label, (width/2 - title_label.get_width()/2, 400))

        # Press S to move DOWN
        title_label = title_font.render("Press S to move BACKWARD", 1, (255,255,255))    
        screen.blit(title_label, (width/2 - title_label.get_width()/2, 450))

        # Press SPACE to SHOOT
        title_label = title_font.render("Press SPACE BAR to SHOOT", 1, (255,255,255))    
        screen.blit(title_label, (width/2 - title_label.get_width()/2, 500))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_loop()
    pygame.quit()       

main_menu()