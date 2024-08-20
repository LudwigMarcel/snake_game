#type: ignore

import pygame
from model import Points, Snake, Food, WallVertical, WallHorizontal

# Constants
SCREEN_SIZE = (512, 512)
SEGMENT_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SNAKE_COLOR = (0, 100, 0)
TICK_RATE = 9
FONT_SIZE = 40


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.background = pygame.image.load('screen_back.jpg').convert()
        self.clock = pygame.time.Clock()
       
        self.snake_segments = pygame.sprite.Group()
        self.food_group = pygame.sprite.GroupSingle()
        self.wall_segment = pygame.sprite.Group()
        self.wall_segment.add(
            WallVertical(220, 100, 150),
            WallVertical(350, 410, 100),
            WallHorizontal(0, 300, 150),
            WallHorizontal(400, 100, 200)
        )

        self.border_wall = pygame.sprite.Group()
        self.border_wall.add(
            WallVertical(0, 0, SCREEN_SIZE[1]),
            WallVertical(SCREEN_SIZE[0] - 10, 0, SCREEN_SIZE[1]),
            WallHorizontal(0, 0, SCREEN_SIZE[0]),
            WallHorizontal(0, SCREEN_SIZE[1] - 10, SCREEN_SIZE[0]))
        
        self.points = Points(10, 10)
        self.points_group = pygame.sprite.GroupSingle(self.points)

        self.direction = pygame.Vector2(SEGMENT_SIZE, 0)
        self.game_on = True
        self.running = True
        self.flag = False

        self.restart_game()
    
    def restart_game(self):
        self.snake_segments.empty()
        self.points.reset()
        initial_pos = [pygame.Vector2(100, 50), pygame.Vector2(85, 50), pygame.Vector2(70, 50)]

        self.head = Snake(initial_pos[0].x, initial_pos[0].y, True)
        self.snake_segments.add(self.head)

        for pos in initial_pos[1:]:
            segment = Snake(pos.x, pos.y)
            self.snake_segments.add(segment)

        self.food_group.add(Food())
        self.check_food_position()

        direction = pygame.Vector2(15, 0)
        self.game_on = True
        self.running = True
        self.flag = False

    def check_food_position(self):
        food = self.food_group.sprite
        while pygame.sprite.spritecollideany(food, self.wall_segment) or pygame.sprite.spritecollideany(food, self.border_wall):
            food.relocate()
    
    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if self.flag and keys[pygame.K_r]:
                print("Restart")
                self.restart_game()

            if self.game_on:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and self.direction.y == 0:
                    self.direction = pygame.Vector2(0, -15)
                if keys[pygame.K_s] and self.direction.y == 0:
                    self.direction = pygame.Vector2(0, 15)
                if keys[pygame.K_a] and self.direction.x == 0:                        
                    self.direction = pygame.Vector2(-15, 0)
                if keys[pygame.K_d] and self.direction.x == 0:
                    self.direction = pygame.Vector2(15, 0)

                self.update_snake()
                self.check_collisions()
                self.draw()

            self.clock.tick(TICK_RATE)

        pygame.quit()
    def update_snake(self):
        new_head_pos = pygame.Vector2(self.head.rect.topleft) + self.direction
        new_head = Snake(new_head_pos[0], new_head_pos[1], True)
        self.snake_segments.add(new_head)

        old_head = self.head
        old_head.__class__ = Snake
        old_head.is_head = False
        old_head.update_image()

        self.snake_segments = pygame.sprite.Group(new_head, *self.snake_segments)
        self.head = new_head

    def check_collisions(self):
        if pygame.sprite.spritecollideany(self.head, self.wall_segment) or pygame.sprite.spritecollideany(self.head, self.border_wall):
            self.game_on = False
            self.flag = True

        if pygame.sprite.spritecollideany(self.head, pygame.sprite.Group(self.snake_segments.sprites()[3:])):
            self.game_on = False
            self.flag = True

        if pygame.sprite.spritecollideany(self.head, self.food_group):
            self.points.increment()
            self.food_group.sprite.relocate()
            self.check_food_position()
        else:
            tail = self.snake_segments.sprites()[-1]
            self.snake_segments.remove(tail)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.snake_segments.draw(self.screen)
        self.food_group.draw(self.screen)
        self.wall_segment.draw(self.screen)
        self.border_wall.draw(self.screen)
        self.points_group.draw(self.screen)

        if self.flag:
            # Draw restart message
            self.font = pygame.font.SysFont(None, 40)
            restart_text = self.font.render('Press R to Restart', True, BLACK)
            self.screen.blit(restart_text, (SCREEN_SIZE[0] // 2 - restart_text.get_width() // 2, SCREEN_SIZE[1] // 2))

        pygame.display.flip()