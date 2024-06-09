import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("xXTankXx")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


FONT = pygame.font.SysFont("comicsans", 30)
pygame.init()


# Tank class
class Tank:
    posx:int
    posy:int
    posz:int
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2, HEIGHT-50, 50, 50)
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

# Bullet class
class Bullet:
    posx:int
    posy:int
    posz:int
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()


def main():
    run = True
    
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False
    
    tank = Tank()
    bullets = []

#UPDATE AND ACTIVE FRAME SOUND
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT,
                                   STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        
        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Shoot a bullet
                bullet = Bullet(tank.rect.centerx, tank.rect.top)
                bullets.append(bullet)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        elif keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        elif keys[pygame.K_UP] and player.x - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        elif keys[pygame.K_DOWN] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.y += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
#GAME OVER CODE HERE
        if hit:
            tankDeathSound = pygame.mixer.Sound('deathsfx.wav')
            tankDeathSound.play()
            

        draw(player, elapsed_time, stars)

#    pygame.quit()


if __name__ == "__main__":
    main()
    