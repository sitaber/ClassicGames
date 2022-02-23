import pygame
import sys
import random
from pygame.locals import *

class Ball():
    def __init__(self):
        self.rect = pygame.Rect(size[0] // 2 , size[1] // 2 , 10, 10)
        self.dx = 4 * random.choice((1,-1))
        self.dy = 4 * random.choice((1,-1))

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= size[1]:
            self.dy *= -1

        if self.rect.colliderect(paddle):
            self.dx *= -1
            self.rect.left = paddle.right

        if self.rect.colliderect(paddle2):
            self.dx *= -1
            self.rect.right = paddle2.left

    def reset(self):
        self.rect.center = (size[0] // 2 , size[1] // 2 )
        self.dx = 4 * random.choice((1,-1))
        self.dy = 4 * random.choice((1,-1))
######### -----------------
# Scores
class ScoreBoard():
    def __init__(self):
        self.surf = pygame.Surface((50,23))
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.text = pygame.font.Font(None, 32)
        self.p1_score = 0
        self.p2_score = 0
        #self.p1_text, self.p2_text = None, None
        self.score_update()

    def p1_scored(self):
        self.p1_score += 1
        self.score_update()

    def p2_scored(self):
        self.p2_score += 1
        self.score_update()

    def score_update(self):
        self.p1_text = self.text.render(f'{self.p1_score}', True, WHITE)
        self.p2_text = self.text.render(f'{self.p2_score}', True, WHITE)

    def reset(self):
        self.p1_score = 0
        self.p2_score = 0
        self.p1_text = self.text.render(f'{self.p1_score}', True, WHITE)
        self.p2_text = self.text.render(f'{self.p2_score}', True, WHITE)
######### -----------------
def player_control():
    # Movement Paddle
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_w]:
        paddle.y += -5
    if pressed_keys[K_s]:
        paddle.y += 5

    if paddle.top < 0:
        paddle.top = 0
    if paddle.bottom > size[1]:
        paddle.bottom = size[1]
######### -----------------
def ai_control():
    if ball.rect.bottom < paddle2.top:
        paddle2.y += -5
    if ball.rect.top > paddle2.bottom:
        paddle2.y += 5

    # Paddle wall collision
    if paddle2.top < 0:
        paddle2.top = 0
    if paddle2.bottom > size[1]:
        paddle2.bottom = size[1]

######### -----------------
# Init
pygame.init()

WHITE = (255, 255, 255)
size = (1200, 700) # Length is 1.8x Width
clock = pygame.time.Clock()

# Display
screen = pygame.display.set_mode((size))

# Players
paddle = pygame.Rect((5,5, 10, 50))
paddle2 = pygame.Rect((size[0] - 15, size[1] - 55, 10 , 50))

# Game Objects
ball = Ball()
score = ScoreBoard()

# Start Menu popup
screen_rect = screen.get_rect()
popup = pygame.Rect((0,0, 200, 100))
popup.center = screen_rect.center

start_font = pygame.font.Font(None, 24)
start_text = start_font.render("Click Box To Start Game", True, (0, 0, 0))
start_rect = start_text.get_rect()
start_rect.center = popup.center
start = False

# Game End
end_text = pygame.font.Font(None, 64)
game_over = end_text.render("Game Over Click Screen To Play Again", True, (0, 0, 0))
over_rect = game_over.get_rect()
over_rect.center = screen_rect.center

# Game loop
while True:
    while not start:
        pygame.draw.rect(screen, (255,255,255), popup)
        screen.blit(start_text, start_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                inbox = popup.collidepoint(pygame.mouse.get_pos())
                if inbox:
                    start = True

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    player_control()
    ai_control()
    ball.update()

    if ball.rect.left > size[0]:
        score.p1_scored()
        ball.reset()

    if ball.rect.right < 0:
        score.p2_scored()
        ball.reset()

    # Draw
    # Main screen
    screen.fill((127, 200, 100))
    pygame.draw.aaline(screen, WHITE, (size[0] // 2, 0), (size[0] // 2, size[1]))
    pygame.draw.circle(screen, WHITE, (size[0] // 2 , size[1] // 2 ), 20 ,  1)

    # Score
    score.surf.fill((0,0,0))
    score.surf.blit(score.p1_text, (score.rect.topleft))
    score.surf.blit(score.p2_text, (score.rect.topright[0] - score.p2_text.get_rect()[2], score.rect[1]))
    screen.blit(score.surf, (size[0] // 2 - 25, 5) )

    # Ball and player objects
    pygame.draw.circle(screen, WHITE, (ball.rect.centerx, ball.rect.centery), 10)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.rect(screen, WHITE, paddle2)

    # Game over
    if abs(score.p1_score - score.p2_score) >= 2 and (score.p1_score >= 11 or score.p2_score >= 11):
        over = True
        while over:
            screen.blit(game_over, over_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    inbox = screen_rect.collidepoint(pygame.mouse.get_pos())
                    if inbox:
                        ball.reset()
                        score.reset()
                        score.surf.fill((0,0,0))
                        score.surf.blit(score.p1_text, (score.rect.topleft))
                        score.surf.blit(score.p2_text, (score.rect.topright[0] - score.p2_text.get_rect()[2], score.rect[1]))
                        screen.blit(score.surf, (size[0] // 2 - 25, 5) )
                        over = False


    pygame.display.update()
    clock.tick(60)
