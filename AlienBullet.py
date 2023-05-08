import pygame

from Constants import WINDOW_HEIGHT


class AlienBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired from the player's ship"""

    def __init__(self, x, y, bullet_group):
        """Initialize the bullet and set starting position"""
        super().__init__()
        self.image = pygame.image.load("assets/red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        """Update the bullet's position"""
        self.rect.y += self.velocity

        # If bullet goes outside screen, kill it
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()