import pygame
import random

pygame.font.init()
POWERUP_FONT = pygame.font.Font(None, 20)

class Paddle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.original_width = 100
        self.height = 10
        self.speed = 7
        self.color = (200, 200, 200)

        self.width = self.original_width
        self.rect = pygame.Rect(
            self.screen_width // 2 - self.width // 2,
            self.screen_height - 30,
            self.width,
            self.height
        )

        self.has_laser = False
    def reset(self):
        self.rect.x = self.screen_width // 2 - self.original_width // 2
        self.width = self.original_width
        self.rect.width = self.width
        self.has_laser = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Ball:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 10
        self.color = (200, 200, 200)
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.is_fireball = False
        self.reset()

    def reset(self):
        self.rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.speed_x = 6 * random.choice((1, -1))
        self.speed_y = -6
        self.is_fireball = False

    def update(self, paddle):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.speed_y *= -1
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.speed_x *= -1

        if self.rect.colliderect(paddle.rect) and self.speed_y > 0:
            self.speed_y *= -1

        if self.rect.top > self.screen_height:
            return 'lost'
        return 'playing'

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)


class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class PowerUp:
    PROPERTIES = {
        'grow': {'color': (60, 60, 255), 'char': 'G'},
        'multi': {'color': (255, 105, 180), 'char': 'M'},
        'shield': {'color': (0, 255, 255), 'char': 'S'},
        'fireball': {'color': (255, 69, 0), 'char': 'F'},
        'laser': {'color': (255, 0, 0), 'char': 'L'},
    }

    def __init__(self, x, y, type):
        self.width = 30
        self.height = 15
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed_y = 3
        self.type = type
        self.color = self.PROPERTIES[type]['color']
        self.char = self.PROPERTIES[type]['char']

    def update(self):
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = POWERUP_FONT.render(self.char, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


class Shield:
    def __init__(self, screen_width, y):
        self.rect = pygame.Rect(0, y, screen_width, 10)
        self.active = True

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (0, 255, 255), self.rect)


class Laser:
    def __init__(self, x, y):
        self.width = 5
        self.height = 15
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (255, 255, 0)
        self.speed_y = -8

    def update(self):
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
