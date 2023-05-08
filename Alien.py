import random

import pygame

from AlienBullet import AlienBullet


class Alien(pygame.sprite.Sprite):
    """This class represents the player's ship"""
    def __init__(self, x, y, velocity, bullet_group):
        """Initialize the alien and set starting positions"""
        super().__init__()
        self.image = pygame.image.load("assets/alien.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.starting_x = x
        self.starting_y = y

        self.direction = 0.5
        self.velocity = velocity
        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound("assets/alien_fire.wav")
        self.shoot_sound.set_volume(0.4)

    def update(self):
        """Update the alien position"""
        self.rect.x += self.direction * self.velocity

        # Randomly fire a bullet
        if random.randint(0, 1000) > 999 and len(self.bullet_group) < 3:
            self.fire()

    def fire(self):
        """Fire a bullet"""
        self.shoot_sound.play()
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def reset(self):
        """Reset the alien position"""
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1