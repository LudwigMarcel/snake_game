import pygame
import random

from pygame.sprite import Group

def check_colision(head_pos, snake_segment, width, height):
    if head_pos <= 0 or head_pos > width-10 or head_pos > height-10 :
        return True 
    for block in snake_segment[1:]:
        if head_pos == block:
            return True

# pygame setup
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('Snake Game')
running = True

#Images
background = pygame.image.load('screen_back.jpg').convert()
apple_image = pygame.image.load('apple.png').convert_alpha()
# create
# snake
class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()     
        self.image =  pygame.Surface([15, 15])
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=(x,y))

# food
class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15,15])
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=(x,y))
    def relocate(self):
        self.rect.topleft = (random.randrange(10, screen.get_width()-10), random.randrange(10, screen.get_height()-10))

snake_segments = pygame.sprite.Group() #grupo de sprites
# criar uma pos inicial, iterar sobre ela, e adicionar um segmento
initial_pos = [pygame.Vector2(100, 50), pygame.Vector2(90, 50), pygame.Vector2(80, 50)]
for pos in initial_pos:
    segment = SnakeSegment(pos.x, pos.y)
    snake_segments.add(segment)
head = snake_segments.sprites()[0] #a cobra sempre vai ser o index 0 no grupo de sprites

# pos init food
food = Food(random.randrange(10, screen.get_width()-10), random.randrange(10, screen.get_height()-10))
food_group = pygame.sprite.GroupSingle(food)

direction = pygame.Vector2(10, 0)
clock = pygame.time.Clock()

while running:  
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and direction.y == 0:
        direction = pygame.Vector2(0, -10)
    if keys[pygame.K_s] and direction.y == 0:
        direction = pygame.Vector2(0, 10)
    if keys[pygame.K_a] and direction.x == 0:
        direction = pygame.Vector2(-10, 0)
    if keys[pygame.K_d] and direction.x == 0:
        direction = pygame.Vector2(10, 0)
    

    #colision check    
    # if check_colision(snake_pos, snake_body, 512, 512):
    #     running = False

    # testar e explicar o funcionamento
    new_head_pos = pygame.Vector2(head.rect.topleft) + direction
    new_head = SnakeSegment(new_head_pos[0], new_head_pos[1])
    snake_segments.add(new_head)
    snake_segments = pygame.sprite.Group(new_head, *snake_segments)
    head = new_head
    
    #check colision border
    #check_colision(head, snake_segments, screen.get_width, screen.get_height)

    # check colision w/ apple
    if pygame.sprite.spritecollideany(head, food_group):
        food.relocate()
    else:  # growth control
        tail = snake_segments.sprites()[-1]
        snake_segments.remove(tail)
        
    
    # fill the screen with a color to wipe away anything from last frame
    screen.blit(background, (0,0))
    snake_segments.draw(screen)
    food_group.draw(screen)
    pygame.display.flip()

    # game speed
    clock.tick(10)

pygame.quit()