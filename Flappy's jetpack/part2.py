# Importing pygame and random
import pygame
import random

# Initializaing the game engine
pygame.init()

# This command will initialize the mixer module
pygame.mixer.init()

# Defining some colours that are used in RGB format
black = (0,0,0)
yellow = (255,215,0)
darkOrange = (255,140,0)
white = (255,255,255)
red = (255,0,0)
gray = (204,186,120)

# --------- !! Importing music and sound effects !! ---------

background_music = pygame.mixer.music.load('Epic Journey - Yung Logos.mp3') # ==> This will load a music filename/file object and prepare it for playback
gameOver_sound = pygame.mixer.Sound('death-sound.mp3')
pygame.mixer.music.play() # ==> This module is to control the playback of music in the sound mixer
gameOver_sound.set_volume(0.1)
pygame.mixer.music.set_volume(0.2) # ==> This will load a sound file, and the sound file will begin as soon as the current sound naturally ends

# -----------------------------------------------------------
# Load the image that is imported to the file's directory
bg = pygame.image.load('picbg.jpg')

# Set the screen caption
screen = pygame.display.set_caption("Flappy's jetpack")

# Deifning some variables for the screen dimensions and the fps (frame/second)
width = 900
height = 500
fps = 65

# Setting the screen dimension and the timer
screen = pygame.display.set_mode((width,height)) 
timer = pygame.time.Clock()

# Defining some variables for the 'Score', 'Restart', and the 'Game over!' texts
font = pygame.font.Font('freesansbold.ttf', 20)
game_over_font = pygame.font.Font('freesansbold.ttf', 30)
restart = pygame.font.Font('freesansbold.ttf', 30)

# -------- !! variables library !! --------

# Coordinations of the player
player_position_x = 255
player_position_y = 255

# Speed and direction of gravity
y_change = 0
jump_height = 12
gravity = .9

# Creating obstacles against the player 
obstacles = [400, 700, 1000, 1300, 1600]
generateObs = True
y_positions = []

# The game isn't over when the player doesn't hit obstacles
game_over = False

# The speed of the player as it moves forward
speed = 3

# The initial score should start from 0
score = 0

# --- DEFINING FUNCTIONS! ---
"""Define a function for the player"""
def draw_player(x_pos, y_pos):
    global y_change 
    mouth = pygame.draw.circle(screen, darkOrange, (x_pos + 25, y_pos +15), 12)
    play = pygame.draw.rect(screen, yellow, [player_position_x, player_position_y, 30, 30], 0, 12)
    eye = pygame.draw.circle(screen, black, (x_pos + 22, y_pos + 12), 5)
    jetpack = pygame.draw.rect(screen, white, [x_pos - 20, y_pos, 18, 28], 3, 2)
    if y_change < 0:
        flame1 = pygame.draw.rect(screen, red, [x_pos - 20, y_pos + 29, 7, 20], 0, 2)
        flame1_yellow = pygame.draw.rect(screen, yellow, [x_pos - 18, y_pos + 30, 3, 18], 0, 2)
        flame2 = pygame.draw.rect(screen, red, [x_pos - 10, y_pos + 29, 7, 20], 0, 2)
        flame2_yellow = pygame.draw.rect(screen, yellow, [x_pos - 8, y_pos + 30, 3, 18], 0, 2)
    return play

"""Define a function for the obstacles"""
def draw_obstacles(obst, y_pos, play):
    global game_over
    for i in range(len(obst)):
        y_coord = y_pos[i]
        top_rect = pygame.draw.rect(screen, gray, [obst[i], 0, 30, y_coord])
        top2 = pygame.draw.rect(screen, gray, [obst[i] -3, y_coord - 20, 36, 20], 0, 5)
        bottom_rect = pygame.draw.rect(screen, gray, [obst[i], y_coord + 200, 30, height - (y_coord + 70)])
        bottom2 = pygame.draw.rect(screen, gray, [obst[i] -3, y_coord + 200, 36, 20], 0, 5)
        if top_rect.colliderect(player) or bottom_rect.colliderect(player):
            game_over = True

"""Define a function for the background image to load on the window"""
def redrawWindow():
    screen.blit(bg, (0,0))

# ---------- MAIN PROGRAM LOOP ----------

running = True
# Keep the loop as long as the user is still playing (running == True)
while running:
    timer.tick(fps) # Start ticking the frame
    redrawWindow() # Call back the function that we created to load the background image.
    if generateObs:
        # Generate obstacles randomly between the range 0 - 300 pixels on y coord
        for i in range(len(obstacles)):
            y_positions.append(random.randint(0, 300))
        generateObs = False

    player = draw_player(player_position_x, player_position_y)
    draw_obstacles(obstacles, y_positions, player)

    # ALL EVENT PROCESSING SHOULD GO below THIS COMMENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                y_change = -jump_height
                
            if event.key == pygame.K_SPACE and game_over:
                player_position_x = 255
                player_position_y = 255
                y_change = 0
                generateObs = True
                obstacles = [400, 700, 1000, 1300, 1600]
                y_positions = [] 
                score = 0
                pygame.mixer.music.play()
                game_over = False

    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT 

    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
    if player_position_y + y_change < height - 30:
        player_position_y += y_change
        y_change += gravity
    else:
        player_position_y = height - 30

    for i in range(len(obstacles)):
        if not game_over:
            obstacles[i] -= speed
            if obstacles[i] < -30:
                obstacles.remove(obstacles[i])
                y_positions.remove(y_positions[i])
                obstacles.append(random.randint(obstacles[-1] + 280, obstacles[-1] + 320) )
                y_positions.append(random.randint(0, 300))
                score += 1
        if game_over:
           gameOver_sound.play()
           gameOver = game_over_font.render("Game over!", True, white)
           screen.blit(gameOver, (350, 250))
           restart = game_over_font.render("Press space to restart", True, white)
           screen.blit(restart, (280, 290))

    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT


    score_text = font.render('Score: ' + str(score), True, white)
    screen.blit(score_text, (10, 450))
    pygame.display.flip()
pygame.quit()