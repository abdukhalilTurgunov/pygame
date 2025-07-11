import pygame
import sys
import random
from game_objects import Paddle, Ball, Brick, PowerUp, Shield, Laser

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Arkanoid by Abdukhalil Turgunov")

# abdukhalil_turgunov@student.itpu.uz

BG_COLOR = pygame.Color('grey12')
BRICK_COLORS = [(178, 34, 34), (255, 165, 0), (255, 215, 0), (50, 205, 50)]
font = pygame.font.Font(None, 40)

# === Sounds ===
try:
    bounce_sound = pygame.mixer.Sound('bounce.wav')
    brick_break_sound = pygame.mixer.Sound('brick_break.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
    laser_sound = pygame.mixer.Sound('laser.wav')
    win_sound = pygame.mixer.Sound('win.mp3')
except pygame.error as e:
    print(f"Sound error: {e}")

    class DummySound:
        def play(self): pass

    bounce_sound = brick_break_sound = game_over_sound = laser_sound = win_sound = DummySound()

# === Game objects ===
paddle = Paddle(screen_width, screen_height)
balls = [Ball(screen_width, screen_height)]
bricks = []
power_ups = []
lasers = []
shield = None

score = 0
lives = 3
current_level = 0
is_muted = False

def create_brick_wall(rows):
    b_list = []
    brick_cols = 10
    brick_width = 75
    brick_height = 20
    brick_padding = 5
    wall_start_y = 50
    for row in range(rows):
        for col in range(brick_cols):
            x = col * (brick_width + brick_padding) + brick_padding
            y = row * (brick_height + brick_padding) + wall_start_y
            color = BRICK_COLORS[row % len(BRICK_COLORS)]
            b_list.append(Brick(x, y, brick_width, brick_height, color))
    return b_list

levels = [4, 6, 8]
bricks = create_brick_wall(levels[current_level])

game_state = 'title'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == 'title':
                    game_state = 'playing'
                elif game_state == 'game_over' or game_state == 'you_win':
                    paddle.reset()
                    balls = [Ball(screen_width, screen_height)]
                    current_level = 0
                    bricks = create_brick_wall(levels[current_level])
                    score = 0
                    lives = 3
                    power_ups.clear()
                    lasers.clear()
                    shield = None
                    game_state = 'title'
            if event.key == pygame.K_m:
                is_muted = not is_muted
            if event.key == pygame.K_r:
                paddle.reset()
                balls = [Ball(screen_width, screen_height)]
                current_level = 0
                bricks = create_brick_wall(levels[current_level])
                score = 0
                lives = 3
                power_ups.clear()
                lasers.clear()
                shield = None
                game_state = 'playing'
            if event.key == pygame.K_f and paddle.has_laser:
                lasers.append(Laser(paddle.rect.centerx - 30, paddle.rect.top))
                lasers.append(Laser(paddle.rect.centerx + 30, paddle.rect.top))
                if not is_muted:
                    laser_sound.play()

    screen.fill(BG_COLOR)

    sound_status_text = "Sound: OFF" if is_muted else "Sound: ON"
    sound_surf = font.render(sound_status_text, True, (255, 255, 255))
    screen.blit(sound_surf, (10, screen_height - 40))

    if game_state == 'title':
        title_surf = font.render("ARKANOID by Abdukhalil", True, (255, 255, 255))
        start_surf = font.render("Press SPACE to Start", True, (255, 255, 255))
        mute_surf = font.render("Press M to Mute", True, (255, 255, 255))
        screen.blit(title_surf, (screen_width//2 - title_surf.get_width()//2, 200))
        screen.blit(start_surf, (screen_width//2 - start_surf.get_width()//2, 300))
        screen.blit(mute_surf, (screen_width//2 - mute_surf.get_width()//2, 350))
    elif game_state == 'playing':
        paddle.update()
        paddle.draw(screen)

        for ball in balls[:]:
            status = ball.update(paddle)
            ball.draw(screen)

            if status == 'lost':
                if shield and shield.active:
                    ball.rect.bottom = shield.rect.top
                    ball.speed_y *= -1
                    shield.active = False
                else:
                    balls.remove(ball)
                    if not balls:
                        lives -= 1
                        if not is_muted:
                            game_over_sound.play()
                        if lives <= 0:
                            game_state = 'game_over'
                        else:
                            balls = [Ball(screen_width, screen_height)]
                            paddle.reset()

        for brick in bricks[:]:
            for ball in balls:
                if ball.rect.colliderect(brick.rect):
                    if not ball.is_fireball:
                        ball.speed_y *= -1
                    if not is_muted:
                        bounce_sound.play()
                    bricks.remove(brick)
                    score += 10
                    if random.random() < 0.3:
                        p_type = random.choice(['grow', 'multi', 'shield', 'fireball', 'laser'])
                        power_ups.append(PowerUp(brick.rect.centerx, brick.rect.centery, p_type))
                    break
            brick.draw(screen)

        for power_up in power_ups[:]:
            power_up.update()
            power_up.draw(screen)
            if paddle.rect.colliderect(power_up.rect):
                if power_up.type == 'grow':
                    paddle.width = 150
                    paddle.rect.width = paddle.width
                elif power_up.type == 'multi':
                    new_ball = Ball(screen_width, screen_height)
                    new_ball.rect.center = balls[0].rect.center
                    new_ball.speed_x = -balls[0].speed_x
                    new_ball.speed_y = balls[0].speed_y
                    balls.append(new_ball)
                elif power_up.type == 'shield':
                    shield = Shield(screen_width, screen_height - 10)
                elif power_up.type == 'fireball':
                    for b in balls:
                        b.is_fireball = True
                elif power_up.type == 'laser':
                    paddle.has_laser = True
                power_ups.remove(power_up)

        for laser in lasers[:]:
            laser.update()
            if laser.rect.bottom < 0:
                lasers.remove(laser)
            else:
                for brick in bricks[:]:
                    if laser.rect.colliderect(brick.rect):
                        bricks.remove(brick)
                        if not is_muted:
                            brick_break_sound.play()
                        score += 10
                        lasers.remove(laser)
                        break
            laser.draw(screen)

        if shield:
            shield.draw(screen)

        if not bricks:
            current_level += 1
            if current_level < len(levels):
                bricks = create_brick_wall(levels[current_level])
                balls = [Ball(screen_width, screen_height)]
                paddle.reset()
            else:
                if not is_muted:
                    win_sound.play()
                game_state = 'you_win'
                bricks.clear()
                
        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_surf = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))
        screen.blit(lives_surf, (screen_width - lives_surf.get_width() - 10, 10))

    elif game_state == 'game_over':
        over_surf = font.render("GAME OVER", True, (255, 255, 255))
        restart_surf = font.render("Press R to Retry or SPACE for Title", True, (255, 255, 255))
        screen.blit(over_surf, (screen_width//2 - over_surf.get_width()//2, 250))
        screen.blit(restart_surf, (screen_width//2 - restart_surf.get_width()//2, 300))

    elif game_state == 'you_win':
        trophy_surf = font.render("TROPHY!!!", True, (255, 215, 0))
        score_surf = font.render(f"Final Score: {score}", True, (255, 255, 255))
        lives_surf = font.render(f"Lives Left: {lives}", True, (255, 255, 255))
        restart_surf = font.render("Press SPACE for Title", True, (255, 255, 255))

        screen.blit(trophy_surf, (screen_width//2 - trophy_surf.get_width()//2, 180))
        screen.blit(score_surf, (screen_width//2 - score_surf.get_width()//2, 250))
        screen.blit(lives_surf, (screen_width//2 - lives_surf.get_width()//2, 300))
        screen.blit(restart_surf, (screen_width//2 - restart_surf.get_width()//2, 350))

    pygame.display.flip()
    clock.tick(60)
