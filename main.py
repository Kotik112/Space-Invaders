import pygame, random

from Alien import Alien
from Game import Game, WINDOW_WIDTH, WINDOW_HEIGHT
from Player import Player

pygame.init()

FPS = 60
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Create bullet groups
player_bullet_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

# Create a player and Player object
player_group = pygame.sprite.Group()
player = Player(player_bullet_group)
player_group.add(player)

# Create an alien group.
# Will add Alien objects via the game's start new round method
alien_group = pygame.sprite.Group()

#TEST ALIENS, DELET LATER
for i in range(10):
    alien = Alien(64 + i * 64, 100, 5, alien_bullet_group)
    alien_group.add(alien)

# Create a Game object
my_game = Game()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    # Fill the display
    display_surface.fill((0, 0, 0))

    # Update and display all sprite groups
    player_group.update()
    player_group.draw(display_surface)

    alien_group.update()
    alien_group.draw(display_surface)

    player_bullet_group.update()
    player_bullet_group.draw(display_surface)

    alien_bullet_group.update()
    alien_bullet_group.draw(display_surface)

    # Update and draw game object
    my_game.update()
    my_game.draw(display_surface)

    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()