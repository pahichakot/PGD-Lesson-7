#Space invaders game
import pygame, os

pygame.font.init()

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Invader Game")

#Colors
WHITE = (255, 255, 255)
PURPLE = (147, 112, 219)
GREEN = (0, 109, 91)
BLACK = (0,0,0)

#Border
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

#Fonts
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VEL = 5 #player velocity
BULLET_VEL = 7
MAX_BULLETS = 3
ALIEN_WIDTH, ALIEN_HEIGHT = 55, 40

#To customize event
GREEN_HIT = pygame.USEREVENT + 1
PURPLE_HIT = pygame.USEREVENT + 2

#Load image from assets folder
GREEN_ALIEN_IMAGE = pygame.image.load(os.path.join("assets", "alien_green.png"))
PURPLE_ALIEN_IMAGE = pygame.image.load(os.path.join("assets", "alien_purple.png"))
SPACE_IMAGE = pygame.image.load(os.path.join("assets", "space.png"))

#Rotates and reduces ALIEN size
GREEN_ALIEN = pygame.transform.rotate(pygame.transform.scale(GREEN_ALIEN_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT)), 90)
PURPLE_ALIEN = pygame.transform.rotate(pygame.transform.scale(PURPLE_ALIEN_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT)), 270)
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

def draw_window(green, purple, green_bullets, purple_bullets, green_health, purple_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    #Purple
    purple_health_text = HEALTH_FONT.render("Health: "+str(purple_health), 1, WHITE)
    WIN.blit(purple_health_text, (700, 10))

    WIN.blit(PURPLE_ALIEN, (purple.x, purple.y))

    for bullet in purple_bullets:
        pygame.draw.rect(WIN, PURPLE, bullet)

    #Green
    green_health_text = HEALTH_FONT.render("Health: "+str(green_health), 1, WHITE)
    WIN.blit(green_health_text, (100, 10))

    WIN.blit(GREEN_ALIEN, (green.x, green.y))

    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()

def handle_bullets(green_bullets, purple_bullets, green, purple):
    
    #Green
    for bullet in green_bullets:
        bullet.x += BULLET_VEL #move right

        if purple.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PURPLE_HIT))
            green_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            green_bullets.remove(bullet)

    #Purple
    for bullet in purple_bullets:
        bullet.x -= BULLET_VEL #move left

        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            purple_bullets.remove(bullet)
        elif bullet.x < 0:
            purple_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))

    pygame.display.update()

    pygame.time.delay(5000)

#Move green alien
def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_a] and green.x - VEL > 0:
        green.x -= VEL
    if keys_pressed[pygame.K_d] and green.x + VEL + green.width < BORDER.x:
        green.x += VEL
    if keys_pressed[pygame.K_w] and green.y - VEL > 0:
        green.y -= VEL
    if keys_pressed[pygame.K_s] and green.y + VEL + green.height < HEIGHT - 15:
        green.y += VEL

#Move purple alien
def purple_handle_movement(keys_pressed, purple):
    if keys_pressed[pygame.K_LEFT] and purple.x - VEL > BORDER.x + BORDER.width:
        purple.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and purple.x + VEL + purple.width < WIDTH:
        purple.x += VEL
    if keys_pressed[pygame.K_UP] and purple.y - VEL > 0:
        purple.y -= VEL
    if keys_pressed[pygame.K_DOWN] and purple.y + VEL + purple.height < HEIGHT - 15:
        purple.y += VEL

def main():
    purple = pygame.Rect(700, 300, ALIEN_WIDTH, ALIEN_HEIGHT)
    green = pygame.Rect(100, 300, ALIEN_WIDTH, ALIEN_HEIGHT)
    green_bullets = []
    purple_bullets = []
    purple_health = 10
    green_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x, green.y, 10, 5)
                    green_bullets.append(bullet)

                if event.key == pygame.K_m and len(purple_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(purple.x, purple.y, 10, 5)
                    purple_bullets.append(bullet)

            if event.type == PURPLE_HIT:
                green_health = green_health - 1

            if event.type == GREEN_HIT:
                purple_health = purple_health - 1

        winner_text = ""

        if purple_health < 0:
            winner_text = "Green Wins!"
        if green_health < 0:
            winner_text = "Purple Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        green_handle_movement(keys_pressed, green)
        purple_handle_movement(keys_pressed, purple)
        handle_bullets(green_bullets, purple_bullets, green, purple)
        draw_window(green, purple, green_bullets, purple_bullets, green_health, purple_health)

    main()

if __name__ == "__main__":
    main()