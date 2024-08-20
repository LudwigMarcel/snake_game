import pygame
import random

#Constants
SCREEN_SIZE = (512, 512)
SEGMENT_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SNAKE_COLOR = (0, 100, 0)

class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y, is_head=False):
        super().__init__()
        self.is_head = is_head
        self.image = pygame.Surface([SEGMENT_SIZE, SEGMENT_SIZE])
        self.update_image()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update_image(self):
        self.image.fill(SNAKE_COLOR)
        if self.is_head:
            pygame.draw.circle(self.image, BLACK, (4, 4), 2)
            pygame.draw.circle(self.image, BLACK, (10, 4), 2)

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([SEGMENT_SIZE, SEGMENT_SIZE])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.relocate()

    def relocate(self):
        self.rect.topleft = (random.randint(0, SCREEN_SIZE[0] - SEGMENT_SIZE), random.randint(0, SCREEN_SIZE[1] - SEGMENT_SIZE))

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