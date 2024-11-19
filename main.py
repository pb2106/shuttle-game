import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pubzee!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BOX1 = pygame.Rect(207,110, 104, 45)
BOX2 = pygame.Rect(30,207, 157, 38)
BOX3 = pygame.Rect(177,270, 104, 45)
BOX4 = pygame.Rect(50,330, 43, 46)
BOX5 = pygame.Rect(423,30, 13, 126)
BOX6 = pygame.Rect(455,267, 73, 48)
BOX7 = pygame.Rect(363,360, 200, 40)
BOX8 = pygame.Rect(735,30, 7, 218)
BOX9 = pygame.Rect(610,80, 165, 45)
BOX10 = pygame.Rect(735,175, 40, 44)
BOX11 = pygame.Rect(578,203, 120, 46)
BOX12 = pygame.Rect(704,220, 8, 150)
BOXES=[BOX1,BOX2,BOX3,BOX4,BOX5,BOX6,BOX7,BOX8,BOX9,BOX10,BOX11,BOX12]

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 3
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 35, 20

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_SPACESHIP_ROTATE=pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 90)


RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'map.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 25:  # LEFT
        if not yellow.collidelistall(BOXES):
            yellow.x -= VEL
        if yellow.collidelistall(BOXES):
            yellow.x += VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < WIDTH-10:  # RIGHT
        if not yellow.collidelistall(BOXES):
            yellow.x += VEL
        if yellow.collidelistall(BOXES):
            yellow.x -= VEL
        
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 30:  # UP
        if not yellow.collidelistall(BOXES):
            yellow.y -= VEL
        if yellow.collidelistall(BOXES):
            yellow.y += VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 75:  # DOWN
        if not yellow.collidelistall(BOXES):
            yellow.y += VEL
        if yellow.collidelistall(BOXES):
            yellow.y -= VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 25:  # LEFT
        if not red.collidelistall(BOXES):
            red.x -= VEL
        if red.collidelistall(BOXES):
            red.x += VEL
            
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH-10:  # RIGHT
        if not red.collidelistall(BOXES):
            red.x += VEL
        if red.collidelistall(BOXES):
            red.x -= VEL
            
    if keys_pressed[pygame.K_UP] and red.y - VEL > 30:  # UP
       if not red.collidelistall(BOXES):
           red.y -= VEL
       if red.collidelistall(BOXES):
           red.y += VEL
            
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 75:  # DOWN
       if not red.collidelistall(BOXES):
           red.y += VEL
       if red.collidelistall(BOXES):
           red.y -= VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
        elif bullet.collidelistall(BOXES):
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        elif bullet.collidelistall(BOXES):
            red_bullets.remove(bullet)
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(800, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(50, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                   

            if event.type == RED_HIT:
                red_health -= 1
           

            if event.type == YELLOW_HIT:
                yellow_health -= 1
              

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
