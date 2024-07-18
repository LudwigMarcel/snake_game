import pygame
import random

from pygame.sprite import Group

def check_colision(head_pos, snake_segment, width, height):
    if head_pos <= 0 or head_pos > width-10 or head_pos > height-10 :
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
class SnakeHead(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill((0, 0, 255))  # Cor azul para a cabeça

        # Desenha os olhos (pequenos círculos brancos)
        pygame.draw.circle(self.image, (0,0,0), (4, 4), 2)  # Olho esquerdo
        pygame.draw.circle(self.image, (0,0,0), (10, 4), 2)  # Olho direito
        
        self.rect = self.image.get_rect(topleft=(x, y))

class SnakeBody(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill((0, 0, 255))  # Cor azul para o corpo

        # Desenha a rajada em tons de azul
        pygame.draw.line(self.image, (0, 0, 200), (0, 0), (15, 15), 6)
        pygame.draw.line(self.image, (0, 55, 255), (3, 3), (10, 10), 2)
        
        self.rect = self.image.get_rect(topleft=(x, y))


# food
class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15,15])
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=(x,y))
    def relocate(self):
        self.rect.topleft = (random.randrange(20, screen.get_width()-20), random.randrange(20, screen.get_height()-20))

class WallVertical(pygame.sprite.Sprite):
    def __init__(self, x ,y) :
        super().__init__()
        self.image = pygame.Surface([1, 512])
        self.image.fill('blue') #da uma cor ao sprite
        self.image.set_colorkey('blue') #usa essa cor de referencia pra sumir o sprite
        self.rect = self.image.get_rect(topleft=(x,y))

class WallHorizontal(pygame.sprite.Sprite):
    def __init__(self, x ,y) :
        super().__init__()
        self.image = pygame.Surface([512, 1])
        self.image.fill('blue')
        self.image.set_colorkey('blue')
        self.rect = self.image.get_rect(topleft=(x,y))

wall_segment = pygame.sprite.Group()
left_wall = WallVertical(17, 0)
right_wall = WallVertical(495,0)
uper_wall = WallHorizontal(0, 17)
down_wall = WallHorizontal(0, 495)
wall_segment.add(left_wall, right_wall, uper_wall, down_wall)

snake_segments = pygame.sprite.Group() #grupo de sprites
# criar uma pos inicial, iterar sobre ela, e adicionar um segmento
initial_pos = [pygame.Vector2(100, 50), pygame.Vector2(85, 50), pygame.Vector2(70, 50)]

head_segment = SnakeHead(initial_pos[0].x, initial_pos[0].y)
snake_segments.add(head_segment)
head = head_segment

for pos in initial_pos:
    segment = SnakeBody(pos.x, pos.y)
    snake_segments.add(segment)
head = snake_segments.sprites()[0] #a cobra sempre vai ser o index 0 no grupo de sprites

# pos init food
food = Food(random.randrange(20, screen.get_width()-20), random.randrange(20, screen.get_height()-20))
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
        running = False

    #check colision self
    snake_body =  pygame.sprite.Group(snake_segments.sprites()[3:])
    if pygame.sprite.spritecollide(head, snake_body, True):
        print("cabeça")
        

    # check colision w/ apple
    if pygame.sprite.spritecollideany(head, food_group):
        food.relocate()
    else:  # growth control
        tail = snake_segments.sprites()[-1]
        snake_segments.remove(tail)
        
    
    #desenha na tela 
    screen.blit(background, (0,0))
    snake_segments.draw(screen)
    food_group.draw(screen)
    wall_segment.draw(screen)
    pygame.display.flip()

    # game speed
    clock.tick(9)

pygame.quit()