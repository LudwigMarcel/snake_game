import pygame
import random

from pygame.sprite import Group

# pygame setup
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('Snake Game')

#Images
background = pygame.image.load('screen_back.jpg').convert()

def check_food_position(food, walls):
    while pygame.sprite.spritecollideany(food, walls):
        food.relocate()

#Restart the game to its original positions
class RestartGame(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([300, 100])
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.font = pygame.font.SysFont(None, 40)
        self.text = self.font.render('Press R to Restart', True, (0, 0, 0))
        self.image.blit(self.text, (20, 40))

def restart_game():
    global snake_segments, head, food, direction, game_on, flag, points_group, points
    snake_segments.empty()
    points.reset()
    initial_pos = [pygame.Vector2(100, 50), pygame.Vector2(85, 50), pygame.Vector2(70, 50)]

    head_segment = SnakeHead(initial_pos[0].x, initial_pos[0].y)
    snake_segments.add(head_segment)
    head = head_segment

    for pos in initial_pos[1:]:
        segment = SnakeBody(pos.x, pos.y)
        snake_segments.add(segment)

    food.relocate()
    direction = pygame.Vector2(15, 0)
    game_on = True
    flag = False

# Create classes
# Create the Snake head and body
class SnakeHead(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill((0,100,0))
        self.rect = self.image.get_rect(topleft=(x, y))
        pygame.draw.circle(self.image, (0, 0, 0), (4, 4), 2)
        pygame.draw.circle(self.image, (0, 0, 0), (10, 4), 2)

class SnakeBody(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill((0,100,0))
        self.rect = self.image.get_rect(topleft=(x, y))
        pygame.draw.line(self.image, (173,255,47), (0, 0), (15, 15), 6)
        pygame.draw.line(self.image, (46,139,87), (3, 3), (10, 10), 2)
        
# Create the apple and relocate when eated
class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15,15], pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        # maçã redonda
        pygame.draw.circle(self.image, (255, 0, 0), (7, 7), 7)
    def relocate(self):
        self.rect.topleft = (random.randrange(25, screen.get_width()-25), random.randrange(25, screen.get_height()-25))

# Create the walls
class WallVertical(pygame.sprite.Sprite):
    def __init__(self, x, y, height):
        super().__init__()
        self.image = pygame.Surface([10, height])
        self.image.fill('black')
        self.rect = self.image.get_rect(topleft=(x, y))

class WallHorizontal(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface([width, 10])
        self.image.fill('black')
        self.rect = self.image.get_rect(topleft=(x, y))

# Points counter
class Points(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 30])
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.font = pygame.font.SysFont(None, 14)
        self.points = 0
        self.update_text()

    def update_text(self):
        self.image.fill("white")
        text = self.font.render(f'Points: {self.points}', True, (0, 0, 0))
        self.image.blit(text, (5, 5))

    def increment(self):
        self.points += 1
        self.update_text()
    
    def reset(self):
        self.points = 0
        self.update_text()

# Position the walls on the screen
border_walls = pygame.sprite.Group()
border_walls.add(
    WallVertical(0, 0, screen.get_height()),       
    WallVertical(screen.get_width() - 10, 0, screen.get_height()), 
    WallHorizontal(0, 0, screen.get_width()),   
    WallHorizontal(0, screen.get_height() - 10, screen.get_width())  
)
wall_segment = pygame.sprite.Group()
wall_segment.add(
    WallVertical(220, 100, 150),
    WallVertical(350, 410, 100),
    WallHorizontal(0, 300, 150),
    WallHorizontal(400, 100, 200)
)

# Create the snake segments, that builds her body
snake_segments = pygame.sprite.Group()
initial_pos = [pygame.Vector2(100, 50), pygame.Vector2(85, 50), pygame.Vector2(70, 50)]
head_segment = SnakeHead(initial_pos[0].x, initial_pos[0].y)
snake_segments.add(head_segment)
head = head_segment

for pos in initial_pos:
    segment = SnakeBody(pos.x, pos.y)
    snake_segments.add(segment)
head = snake_segments.sprites()[0] # head will always be the index 0

# pos init food
food = Food(random.randrange(25, screen.get_width()-25), random.randrange(25, screen.get_height()-25))
food_group = pygame.sprite.GroupSingle(food)

rect_msg = RestartGame((screen.get_width()/2) -125, (screen.get_height()/2)-50)
rect_msg_group = pygame.sprite.Group(rect_msg)

points = Points(10, 10)
points_group = pygame.sprite.GroupSingle(points)

direction = pygame.Vector2(10, 0)
clock = pygame.time.Clock()
flag = False
running = True
game_on = True
while running:  
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if flag and keys[pygame.K_r]:
        restart_game()

    if game_on:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and direction.y == 0:
            direction = pygame.Vector2(0, -15)
        if keys[pygame.K_s] and direction.y == 0:
            direction = pygame.Vector2(0, 15)
        if keys[pygame.K_a] and direction.x == 0:
            direction = pygame.Vector2(-15, 0)
        if keys[pygame.K_d] and direction.x == 0:
            direction = pygame.Vector2(15, 0)
        
    #a cada frame cria uma nova posição pra cabeca da cobra e atualiza o corpo em relaçao a cabeça
        new_head_pos = pygame.Vector2(head.rect.topleft) + direction
        new_head = SnakeHead(new_head_pos[0], new_head_pos[1])
        snake_segments.add(new_head)
    #pega a referencia da cabeça no frame antrior, atribui a uma nova variavel, modifica a cabeça pra ser corpo agora e atualiza
        old_head = head
        old_head.__class__ = SnakeBody  # Muda a classe do antigo head para SnakeBody
        old_head.image = SnakeBody(old_head.rect.x, old_head.rect.y).image  # Atualiza a imagem para a do corpo
    #adiciona cabeça e corpo no grupo que forma a cobra
        snake_segments = pygame.sprite.Group(new_head, *snake_segments)
        head = new_head
        
        #check colision border
        if pygame.sprite.spritecollideany(head, wall_segment):
            game_on = False
            flag = True
        if pygame.sprite.spritecollideany(head, border_walls):
            game_on = False
            flag = True

        #check colision self
        snake_body =  pygame.sprite.Group(snake_segments.sprites()[3:])
        if pygame.sprite.spritecollide(head, snake_body, True):
            game_on = False
            flag = True

        # check colision w/ apple
        if pygame.sprite.spritecollideany(head, food_group):
            points.increment()
            food.relocate()
            check_food_position(food, wall_segment)
            check_food_position(food, border_walls)

        else:  # growth control
            tail = snake_segments.sprites()[-1]
            snake_segments.remove(tail)

    #desenha na tela 
    screen.blit(background, (0, 0))
    snake_segments.draw(screen)
    food_group.draw(screen)
    wall_segment.draw(screen)
    points_group.draw(screen)
    border_walls.draw(screen)
    if flag:
        rect_msg_group.draw(screen)
    pygame.display.flip()

    # game speed
    clock.tick(9)

pygame.quit()