import pygame
import time
import random
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
PLAYER_WIDTH = 45
PLAYER_HEIGHT = 45
PLAYER_VEL = 3.2
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3
FONT = pygame.font.SysFont("comicsans", 30)
FIRING_COOLDOWN = 0.25
PLAYER1FIRE = pygame.K_x
PLAYER2FIRE = pygame.K_b
PLAYER3FIRE = pygame.K_m
PLAYER4FIRE = pygame.K_KP0

victoryWait = 4
from moviepy.editor import *

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("xXTankXx")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))
bullet_image = pygame.image.load("bullet.png")

tank_images = {
    'tank1': {
        'up': pygame.image.load("tank_up.png"),
        'down': pygame.image.load("tank_down.png"),
        'left': pygame.image.load("tank_left.png"),
        'right': pygame.image.load("tank_right.png")
    },
    'tank2': {
        'up': pygame.image.load("tank2_up.png"),
        'down': pygame.image.load("tank2_down.png"),
        'left': pygame.image.load("tank2_left.png"),
        'right': pygame.image.load("tank2_right.png")
    },
    'tank3': {
        'up': pygame.image.load("tank3_up.png"),
        'down': pygame.image.load("tank3_down.png"),
        'left': pygame.image.load("tank3_left.png"),
        'right': pygame.image.load("tank3_right.png")
    },
    'tank4': {
        'up': pygame.image.load("tank4_up.png"),
        'down': pygame.image.load("tank4_down.png"),
        'left': pygame.image.load("tank4_left.png"),
        'right': pygame.image.load("tank4_right.png")
    }
}

# Load wall images
brick_image = pygame.image.load("brick.png")
breaking_images = [pygame.image.load(f"break_{i}.png") for i in range(3)]

# Map layout (0 = empty space, 1 = wall)
mapID = random.randint(0,3)
# mapID = 3
match mapID:
    case 0:
        MAP = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        ]

    case 1:
        MAP = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
]


    case 2:
        MAP = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]
    case 3:
        MAP = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
]
TILE_SIZE = WIDTH // len(MAP[0])

# Wall class
class Wall:
    def __init__(self, x, y):
        self.image = brick_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = len(breaking_images)  # Number of breaking stages

    def hit(self):
        self.health -= 1
        if self.health > 0:
            self.image = breaking_images[len(breaking_images) - self.health - 1]

    def is_broken(self):
        return self.health <= 0

    def draw(self, screen):
        if self.health > 0:
            screen.blit(self.image, self.rect)

# Tank class
class Tank:
    def __init__(self, up_key, down_key, left_key, right_key, images):
        self.images = images  # Dictionary of images for this tank
        self.image = pygame.transform.scale(self.images['up'], (PLAYER_WIDTH, PLAYER_HEIGHT))  # Default image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = PLAYER_VEL
        self.direction = 'up'  # Default direction
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key
        self.ID = 0
        self.isDestroyed = 0

        self.moveSound = pygame.mixer.Sound('move.ogg')
        self.moveSound.set_volume(0.3)
        self.moveSoundCooldown = 0.5  # Default cooldown duration
        self.timeDeltaCapture = time.time() 
        self.tankFireLastTime = time.time()
        self.health = 1  # Add health attribute to the tank (you can adjust as needed)
        
    def move(self, keys):
        initial_position = self.rect.topleft
        if(self.isDestroyed == 0):
            if keys[self.left_key]:
                if self.rect.x - self.speed >= 0:
                    self.rect.x -= self.speed
                    self.image = pygame.transform.scale(self.images['left'], (PLAYER_WIDTH, PLAYER_HEIGHT))
                    self.direction = 'left'
                    if time.time() > self.timeDeltaCapture:
                        pygame.mixer.Sound.play(self.moveSound)
                        self.timeDeltaCapture = time.time() + self.moveSound.get_length()  # Reset the cooldown based on sound length

            elif keys[self.right_key]:
                if self.rect.x - self.speed >= 0:
                    self.rect.x += self.speed
                    self.image = pygame.transform.scale(self.images['right'], (PLAYER_WIDTH, PLAYER_HEIGHT))
                    self.direction = 'right'
                    if time.time() > self.timeDeltaCapture:
                        pygame.mixer.Sound.play(self.moveSound)
                        self.timeDeltaCapture = time.time() + self.moveSound.get_length()  # Reset the cooldown based on sound length

            elif keys[self.up_key]:
                if self.rect.y - self.speed >= 0:
                    self.rect.y -= self.speed
                    self.image = pygame.transform.scale(self.images['up'], (PLAYER_WIDTH, PLAYER_HEIGHT))
                    self.direction = 'up'
                    if time.time() > self.timeDeltaCapture:
                        pygame.mixer.Sound.play(self.moveSound)
                        self.timeDeltaCapture = time.time() + self.moveSound.get_length()  # Reset the cooldown based on sound length

            elif keys[self.down_key]:
                if self.rect.y + self.speed + self.rect.height <= HEIGHT:
                    self.rect.y += self.speed
                    self.image = pygame.transform.scale(self.images['down'], (PLAYER_WIDTH, PLAYER_HEIGHT))
                    self.direction = 'down'
                    if time.time() > self.timeDeltaCapture:
                        pygame.mixer.Sound.play(self.moveSound)
                        self.timeDeltaCapture = time.time() + self.moveSound.get_length()  # Reset the cooldown based on sound length


            # Collision detection with walls
            for wall in walls:
                if self.rect.colliderect(wall.rect) and not wall.is_broken():
                    self.rect.topleft = initial_position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            return True  # Indicate that the tank is destroyed
        return False  # Tank is still alive

# Bullet class
class Bullet:
    def __init__(self, x, y, direction, parent_tank):
        self.speed = 4
        self.direction = direction
        self.parent_tank = parent_tank
        if self.direction == 'up':
            self.image = bullet_image
        elif self.direction == 'down':
            self.image = pygame.transform.rotate(bullet_image, 180)
        elif self.direction == 'left':
            self.image = pygame.transform.rotate(bullet_image, 90)
        elif self.direction == 'right':
            self.image = pygame.transform.rotate(bullet_image, -90)
        self.rect = self.image.get_rect(center=(x, y))
        self.shootSound = pygame.mixer.Sound('fire.ogg')
        self.active = True  # Indicates if the bullet is still active

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, tanks):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                wall.hit()
                if wall.is_broken():
                    walls.remove(wall)
                return True

        # Check collision with other tanks
        for tank in tanks:
            if tank != self.parent_tank and self.rect.colliderect(tank.rect):
                if tank.take_damage():
                    tank.isDestroyed = 1 # Remove tank if destroyed
                    tank.rect.x = 1100
                    tank.rect.y = 850

                return True

        return False

# Draw function
def draw(tanks, bullets, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    #time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    #WIN.blit(time_text, (10, 10))

    for tank in tanks:
        tank.draw(WIN)

    for bullet in bullets:
        bullet.draw(WIN)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    for wall in walls:
        wall.draw(WIN)

    pygame.display.update()

def update_bullets(bullets):
    count = len(bullets)
    for i in range(count):
        if not bullets[i].active:
            continue
        bullets[i].update()
        
        # Check for collisions with other bullets
        for j in range(count):
            if i != j and bullets[j].active and bullets[i].rect.colliderect(bullets[j].rect):
                bullets[i].active = False
                bullets[j].active = False
                break  # Stop checking other bullets for this one since it's already collided

    # Remove inactive bullets
    bullets[:] = [b for b in bullets if b.active and b.rect.bottom >= 0 and b.rect.top <= HEIGHT and b.rect.right >= 0 and b.rect.left <= WIDTH]


# Main 
def main():
    global walls  # Define the walls list
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    
    startSound= pygame.mixer.Sound('gamestart.wav')
    startSound.set_volume(0.15)
    pygame.mixer.Sound.play(startSound)
    stars = []
    bullets = []

    tank_controls = [
        (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, tank_images['tank1']),  # Arrow keys for tank 1
        (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, tank_images['tank2']),             # WASD for tank 2
        (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, tank_images['tank3']),             # IJKL for tank 3
        (pygame.K_t, pygame.K_g, pygame.K_f, pygame.K_h, tank_images['tank4'])              # TFGH for tank 4
    ]

    tanks = [Tank(*controls) for controls in tank_controls]

    tanks[0].rect.x = 50
    tanks[0].rect.y = 0
    tanks[0].ID = 0

    tanks[1].rect.x = 50
    tanks[1].rect.y = 750
    tanks[1].ID = 1

    tanks[2].rect.x = 900
    tanks[2].rect.y = 0
    tanks[1].ID = 2

    tanks[3].rect.x = 900
    tanks[3].rect.y = 750
    tanks[1].ID = 3

    # Initialize walls
    walls = []
    for row in range(len(MAP)):
        for col in range(len(MAP[0])):
            if MAP[row][col] == 1:
                wall = Wall(col * TILE_SIZE, row * TILE_SIZE)
                walls.append(wall)

    while run:
        aliveIndex = 4
        for tank in tanks:
            if(tank.isDestroyed):
                aliveIndex -=1
        if(aliveIndex == 1 or aliveIndex == 0):
            clip = VideoFileClip("victory" + str(random.randint(1,5)) + ".mp4")
            clip.preview(fps = 20)
            #main()
            break
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if(tanks[1] != None):
                    if time.time() > tanks[1].tankFireLastTime and tanks[1].isDestroyed == 0:
                        if event.key == PLAYER1FIRE and tanks[1].ID == 3:
                            bullet = Bullet(tanks[1].rect.centerx, tanks[1].rect.centery, tanks[1].direction, tanks[1])
                            bullets.append(bullet)
                            pygame.mixer.Sound.play(bullet.shootSound)
                            tanks[1].tankFireLastTime = time.time() + FIRING_COOLDOWN
                if(tanks[0] != None):
                    if time.time() > tanks[0].tankFireLastTime and tanks[0].isDestroyed == 0:
                        if event.key == PLAYER4FIRE and tanks[0].ID == 0:
                            bullet = Bullet(tanks[0].rect.centerx, tanks[0].rect.centery, tanks[0].direction, tanks[0])
                            bullets.append(bullet)
                            pygame.mixer.Sound.play(bullet.shootSound)
                            tanks[0].tankFireLastTime = time.time() + FIRING_COOLDOWN
                if(tanks[2] != None):
                    if time.time() > tanks[2].tankFireLastTime and tanks[2].isDestroyed == 0:
                        if event.key == PLAYER3FIRE and tanks[2].ID == 0:
                            bullet = Bullet(tanks[2].rect.centerx, tanks[2].rect.centery, tanks[2].direction, tanks[2])
                            bullets.append(bullet)
                            pygame.mixer.Sound.play(bullet.shootSound)
                            tanks[2].tankFireLastTime = time.time() + FIRING_COOLDOWN
                if(tanks[3] != None):
                    if time.time() > tanks[3].tankFireLastTime and tanks[3].isDestroyed == 0:
                        if event.key == PLAYER2FIRE and tanks[3].ID == 0:
                            bullet = Bullet(tanks[3].rect.centerx, tanks[3].rect.centery, tanks[3].direction, tanks[3])
                            bullets.append(bullet)
                            pygame.mixer.Sound.play(bullet.shootSound)
                            tanks[3].tankFireLastTime = time.time() + FIRING_COOLDOWN



        keys = pygame.key.get_pressed()
        for tank in tanks:
            tank.move(keys)

        for bullet in bullets[:]:
            bullet.update()
            if (bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT or 
                bullet.rect.right < 0 or bullet.rect.left > WIDTH or 
                bullet.check_collision(tanks)):
                bullets.remove(bullet)
                

        update_bullets(bullets)
        draw(tanks, bullets, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()