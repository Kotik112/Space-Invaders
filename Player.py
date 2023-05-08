import pygame
from Constants import WINDOW_WIDTH, WINDOW_HEIGHT, MOVEMENT_THRESHOLD
from PlayerBullet import PlayerBullet


class Player(pygame.sprite.Sprite):
    """This class represents the player's ship"""
    def __init__(self, bullet_group):
        """Initialize the player and set starting position"""
        super().__init__()
        self.image = pygame.image.load("assets/player_ship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH / 2
        self.rect.bottom = WINDOW_HEIGHT

        # Player stats
        self.lives = 5
        self.velocity = 8

        self.bullet_group = bullet_group
        self.shoot_sound = pygame.mixer.Sound("assets/player_fire.wav")
        self.shoot_sound.set_volume(0.5)

    def update(self):
        """Update the player's position"""
        player_movement_threshold = MOVEMENT_THRESHOLD
        keys = pygame.key.get_pressed()

        # Move the player within the bounds of the game
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_w] and self.rect.top > player_movement_threshold:
            self.rect.y -= self.velocity
        if keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.velocity

    def fire(self):
        """Fire a bullet"""
        #Restrict the number of bullets at a time
        if len(self.bullet_group) < 2:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)

    def reset(self):
        """Reset the player's position"""
        self.rect.centerx = WINDOW_WIDTH / 2
        self.rect.bottom = WINDOW_HEIGHT