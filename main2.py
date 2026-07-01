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
    pygame.draw.Rect(WIN, BLACK, BORDER)

    #Purple
    purple_health_text = HEALTH_FONT.render("Health: "+str(purple_health), 1, WHITE)
    WIN.blit(purple_health_text, (700, 10))

    WIN.blit(PURPLE_ALIEN, (purple.x, purple.y))

    for bullet in purple_bullets:
        pygame.draw.Rect(WIN, PURPLE, bullet)

    #Green
    green_health_text = HEALTH_FONT.render("Health: "+str(green_health), 1, WHITE)
    WIN.blit(green_health_text, (100, 10))

    WIN.blit(GREEN_ALIEN, (green.x, green.y))

    for bullet in green_bullets:
        pygame.draw.Rect(WIN, GREEN, bullet)

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