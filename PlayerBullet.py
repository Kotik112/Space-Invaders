import pygame.sprite


class PlayerBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired from the player's ship"""

    def __init__(self, x, y, bullet_group):
        """Initialize the bullet and set starting position"""
        super().__init__()
        self.image = pygame.image.load("assets/green_laser.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        """Update the bullet's position"""
        self.rect.y -= self.velocity

        # If the bullet is off the screen, kill it
        if self.rect.bottom < 0:
            self.kill()



