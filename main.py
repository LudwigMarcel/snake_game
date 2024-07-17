import pygame
import random

def snake_move():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if player_pos.y > 0:
            player_pos.y -= 10
    if keys[pygame.K_s]:
        if player_pos.y < 480:
            player_pos.y += 10 
    if keys[pygame.K_a]:
        if player_pos.x > 0:
            player_pos.x -= 10
    if keys[pygame.K_d]:
        if player_pos.x < 720:
            player_pos.x += 10

def snake_create(): #useful?
    snake_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    snake_body = ... #TODO
    return snake_pos, snake_body

def snake_grow():
    ...

def check_colision(snake_pos, width, height):
    if snake_pos[0] <= 0 or snake_pos[1] <= 0 or snake_pos[0] > width-10 or snake_pos[1] > height-10 :
        print("bateu")
        return True 
    
def food_colision(snake_pos, food_pos):
    if snake_pos == food_pos: # dont work vector must be exactly one above the other CHANGE
        print("food")
        return True

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()
running = True
dt = 0

food_exist = True

# create an apple
food_pos = pygame.Vector2(random.randrange(1, screen.get_width()), random.randrange(1, screen.get_height()))

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:

    # end_game = pygame.display.set_mode(150,75)
    # end_game.fill("white")
    # pygame.show(end_game)

    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    # functions
    snake_move()
    food_colision(player_pos, food_pos)
    if check_colision(player_pos, 720, 480):
        running = False
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", food_pos, 30)

    pygame.draw.circle(screen, "red", player_pos, 40)

    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()