import pygame
from constants import PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_MAX_ACCELERATION, SCREEN_WIDTH, SCREEN_HEIGHT
from objects.circleshape import CircleShape
from objects.shot import Shot
from objects.defaultweapon import DefaultWeapon
from objects.shotgunweapon import ShotgunWeapon

# Player class for game objects
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.__lives = 3
        self.rotation = 0
        self.accelaration = 1
        self.__previous_dt = 0
        self.current_weapon = DefaultWeapon()

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.get_color(), self.triangle(), 2)

    def get_color(self):
        if self.__lives == 3:
            return "green"
        if self.__lives == 2:
            return "yellow"
        
        return "red"

    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED

    def move(self, dt):  
        if (dt < 0 and self.__previous_dt < 0) or (dt >= 0 and self.__previous_dt >= 0):
            if self.accelaration < PLAYER_MAX_ACCELERATION:
                self.accelaration = self.accelaration + abs(dt) if self.accelaration + abs(dt) < PLAYER_MAX_ACCELERATION else PLAYER_MAX_ACCELERATION

        
        self.__previous_dt = dt
            
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * self.accelaration * dt
        new_x = self.position.x
        new_y = self.position.y
        if new_x < 0:
            new_x = 0
        elif new_x > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH
        
        if new_y < 0:
            new_y = 0
        elif new_y > SCREEN_HEIGHT:
            new_y = SCREEN_HEIGHT

        self.position = pygame.Vector2(new_x, new_y)


    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.current_weapon.shoot(self.position.x, self.position.y, self.rotation)

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.__previous_dt = 0
            self.accelaration = 1

    def take_damage(self):
        self.__lives -= 1
        if self.__lives == 2:
            self.current_weapon = ShotgunWeapon()
        else:
            self.current_weapon = DefaultWeapon()

    def is_alive(self):
        return self.__lives > 0