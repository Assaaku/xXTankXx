import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3
FONT = pygame.font.SysFont("comicsans", 30)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("xXTankXx")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))
bullet_image = pygame.image.load("bullet.png")

# Tank class
class Tank:
    facingDirection:int = 0
    def __init__(self):
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = PLAYER_VEL

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x - self.speed >= 0:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.x + self.speed + self.rect.width <= WIDTH:
            self.rect.x += self.speed
        elif keys[pygame.K_UP] and self.rect.y - self.speed >= 0:
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN] and self.rect.y + self.speed + self.rect.height <= HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Bullet class
class Bullet:
    # shootingDirection = 0
    def __init__(self, x, y):
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7

    def update(self):
        # if(shootingDirection)
        self.rect -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

#draw function
def draw(tank, bullets, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    tank.draw(WIN)

    for bullet in bullets:
        bullet.draw(WIN)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

# Main 
def main():
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    bullets = []
    tank = Tank()

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    bullet = Bullet(tank.rect.centerx, tank.rect.top)
                    bullets.append(bullet)

        keys = pygame.key.get_pressed()
        tank.move(keys)

        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        draw(tank, bullets, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()
