import pygame, sys

# boarders
class Boarder():
    def __init__(self):
        super().__init__()
        self.left_wall = pygame.Rect( (0, 0, 20, size[1]) )
        self.right_wall = pygame.Rect( (size[0] - 20, 0, 20, size[1]) )
        self.top_wall = pygame.Rect( (0, 0, size[0], 14 ) )
        self.color = (128,128,128)

    def draw_boarder(self):
        pygame.draw.rect(screen, self.color, self.left_wall)
        pygame.draw.rect(screen, self.color, self.right_wall)
        pygame.draw.rect(screen, self.color, self.top_wall)

# Ball
class Ball():
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(paddle.rect.midtop[0] - 10, paddle.rect.midtop[1] - 20, 20, 20)
        self.color = (192, 192, 192)
        self.dx = 0
        self.dy = 0
        self.bricks = None
        self.bricks2 = None
        self.hit_top = False
        self.num_hits = 0
        self.hit_red, self.hit_orange = False, False
        self.start = True

    def update(self):
        if self.start == True:
            self.rect.x = paddle.rect.midtop[0] - 10
            self.rect.y = paddle.rect.midtop[1] - 20
        else:
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.collisions()
            self.reflect()

    def draw_ball(self):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def collisions(self):
        if self.rect.colliderect(paddle.rect):
            if abs(paddle.rect.bottom - self.rect.top) < 20 and self.dy < 0:
                self.dy *= -1
            if abs(paddle.rect.top - self.rect.bottom) < 20 and self.dy > 0:
                self.dy *= -1
            if abs(paddle.rect.left - self.rect.right) < 20 and self.dx > 0:
                self.dx *= -1
            if abs(paddle.rect.right - self.rect.left) < 20 and self.dx < 0:
                self.dx *= -1

        if self.rect.colliderect(boarder.right_wall) and self.dx > 0:
            self.dx *= -1
        if self.rect.colliderect(boarder.left_wall) and self.dx < 0:
            self.dx *= -1
        if self.rect.colliderect(boarder.top_wall) and self.dy < 0:
            if self.hit_top == False:
                paddle.rect.w *= 0.5
                self.hit_top = True
            else: self.dy *= -1

        if self.rect.y >= size[1] - 20:
            self.dy *= -1
            if score_board.lives_left >= 0:
                self.start = True
                score_board.lives = score_board.lives[:-1]
                score_board.update()
                self.dy *= -1
            if score_board.lives_left == 0: # need to stop the game
                score_board.update()
                score_board.draw()
                game_state.game_over()


    def reflect(self):
        bricks_copy = []
        for i, brick in enumerate(self.bricks):
            if not ball.rect.colliderect(brick.rect):
                bricks_copy.append(self.bricks[i])

            if self.rect.colliderect(brick.rect):
                score_board.score += brick.point_val
                score_board.update()
                self.num_hits += 1
                if self.num_hits == 4 or self.num_hits == 12:
                    self.dx, self.dy = int(self.dx * 1.25), int(self.dy * 1.25)

                if brick.color == ORANGE and self.hit_orange == False:
                    self.hit_orange = True
                    self.dx, self.dy = int(self.dx * 1.25), int(self.dy * 1.25)
                if brick.color == RED and self.hit_red == False:
                    self.hit_red = True
                    self.dx, self.dy = int(self.dx * 1.25), int(self.dy * 1.25)

                if abs(brick.rect.bottom - self.rect.top) < 20 and self.dy < 0:
                    self.dy *= -1
                if abs(brick.rect.top - self.rect.bottom) < 20 and self.dy > 0:
                    self.dy *= -1
                if abs(brick.rect.left - self.rect.right) < 20 and self.dx > 0:
                    self.dx *= -1
                if abs(brick.rect.right - self.rect.left) < 20 and self.dx < 0:
                    self.dx *= -1

        self.bricks = bricks_copy
        if len(self.bricks) == 0:
            game_state.reset()

# Bricks
class Brick():
    def __init__(self, x_loc, y_loc, color, points):
        super().__init__()
        self.rect = pygame.Rect(x_loc, y_loc, 42, 18)
        self.color = color
        self.point_val = points
        self.speed_multi = 1

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        #pygame.draw.rect(screen, (255,255,255), self.rect, 1)

class Paddle():
    def __init__(self):
        self.color = (0,0,255)
        self.rect = pygame.Rect( (size[0]/2, 850, 42 * 2, 20) )

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            self.rect.x += -8
        if pressed_keys[pygame.K_d]:
            self.rect.x += 8

        if pressed_keys[pygame.K_SPACE] and ball.start == True:
            current_speed = [ball.dx, ball.dy]
            ball.start = False
            if current_speed[0] == 0:
                ball.dx = 5
                ball.dy = 5
            else:
                ball.dx = current_speed[0]
                ball.dy = current_speed[1]

        if self.rect.left <=  20:
            self.rect.left = 20
        if self.rect.right > size[0] - 20:
            self.rect.right = size[0] - 20

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect )


class ScoreBoard():
    font_path = './assets/DejaVuSans.ttf'
    def __init__(self):
        self.text_font = pygame.font.Font(ScoreBoard.font_path , 12)
        self.text_font.set_bold(True)
        self.score_text = self.text_font.render('SCORE', True, (192, 192, 192))
        self.lives_text = self.text_font.render('LIVES', True, (192, 192, 192))
        #
        self.update_font = pygame.font.Font(ScoreBoard.font_path, 32)
        self.update_font.set_bold(True)
        #
        self.score = 0
        self.score_to_text = f'{self.score:0>3}'
        self.lives = '|||'
        self.lives_left = len(self.lives)

    def update(self):
        self.score_to_text = f'{self.score:0>3}'
        self.lives_left = len(self.lives)

    def draw(self):
        # Score Text area
        pygame.draw.rect(screen, (192,192,192), (56, 28, 8, 15))
        pygame.draw.rect(screen, (192,192,192), (56, 27, 58, 1))
        screen.blit(self.score_text, (70,30))
        # Lives text area
        pygame.draw.rect(screen, (192,192,192), (size[0] - 100 - 14, 28, 8, 15))
        pygame.draw.rect(screen, (192,192,192), (size[0] - 100 - 14, 27, 50, 1))
        screen.blit(self.lives_text, (size[0] - 100, 30))
        #
        score_update = self.update_font.render(self.score_to_text, True, (192, 192, 192))
        screen.blit(score_update, (60,44))
        #
        lives_update = self.update_font.render(self.lives, True, (192, 192, 192))
        screen.blit(lives_update, (size[0] - 102,44))

# Game State
class GameState():
    def __init__(self):
        self.state = 'start'
        self.level = 1

    def screen_one(self):
        if self.state == 'start':
            # Draw stuff
            screen.fill((0, 0, 0))
            # Score / Lives
            score_board.draw()
            # Objects
            boarder.draw_boarder()
            paddle.draw()
            ball.draw_ball()

            for brick in ball.bricks:
                brick.draw()

            ball.update()
            paddle.update()

    def reset(self):
        self.level += 1
        if self.level < 3:
            paddle.rect.w *= 2
            ball.dx = 0
            ball.dy = 0
            ball.bricks = ball.bricks2
            ball.hit_top = False
            ball.num_hits = 0
            ball.hit_red, ball.hit_orange = False, False
            ball.start = True
        else: self.game_over()

    def game_over(self):
        self.state = 'over'
        screen.fill((0, 0, 0))
        boarder.draw_boarder()
        score_board.draw()
        paddle.draw()
        ball.draw_ball()

        for brick in ball.bricks:
            brick.draw()

        screen.blit(image, (0,0))
        # Add gameover image
        #print('Game Over')

#### ----------------
def make_bricks(row, color, points):
    # start x + (brick_w + gap) * i | gap = 3
    brick_list = []
    for r in range(row):
        for i in range(14): #
            brick_i = Brick(23 + 45 * i , 100 + r * 21, color[r], points[r])
            brick_list.append(brick_i)
    return brick_list

# Setup
pygame.init()
clock = pygame.time.Clock()
size =  (673, 970) # 673,800 / 673,969.8
screen = pygame.display.set_mode((size))

image = pygame.image.load('./assets/gameover.png')

# Objects
boarder = Boarder()
paddle = Paddle()
ball = Ball()
score_board = ScoreBoard()
#brick
RED = (255,0, 0)
ORANGE = (255, 128, 0)
GREEN = (0, 128, 0)
YELLOW =  (235, 235, 0)

point_vals = [7, 7, 5, 5, 3, 3, 1, 1]
colors = [RED, RED, ORANGE, ORANGE, GREEN, GREEN, YELLOW, YELLOW]
ball.bricks = make_bricks(8, colors, point_vals)
ball.bricks2 = ball.bricks
game_state = GameState()
# DEBUG ------------------
#print(score_board.font_path)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game_state.screen_one()

    pygame.display.update()
    clock.tick(60)
