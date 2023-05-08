import sys, os

import pygame.mixer

from Alien import Alien
from Constants import WINDOW_WIDTH, MOVEMENT_THRESHOLD, WINDOW_HEIGHT, STARTING_ROUND_NUMBER, STARTING_SCORE, \
    STARTING_LIVES


class Game:
    """A class to help control and update gameplay"""
    def __init__(self, player, alien_group, bullet_group, alien_bullet_group, display_surface):
        """initialize game settings"""
        self.round_number = STARTING_ROUND_NUMBER
        self.score = STARTING_SCORE

        self.player = player
        self.alien_group = alien_group
        self.bullet_group = bullet_group
        self.alien_bullet_group = alien_bullet_group

        # Setup sounds
        self.new_round_sound = pygame.mixer.Sound("assets/new_round.wav")
        self.new_round_sound.set_volume(0.5)

        self.breach_sound = pygame.mixer.Sound("assets/breach.wav")
        self.breach_sound.set_volume(0.5)

        self.player_hit_sound = pygame.mixer.Sound("assets/player_hit.wav")
        self.player_hit_sound.set_volume(0.5)

        self.alien_hit_sound = pygame.mixer.Sound("assets/alien_hit.wav")
        self.alien_hit_sound.set_volume(0.5)

        # Set font
        self.font = pygame.font.Font("assets/Facon.ttf", 32)

        # Set display surface
        self.display_surface = display_surface

        # Read high score from file
        self.high_score = self.read_high_score()


    def update(self):
        """update the game"""
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completion()

    def draw(self, display_surface):
        """Draw HUD and other information to display"""
        # Set colors
        WHITE = (255, 255, 255)

        # Set text
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.top = 10
        score_rect.x = WINDOW_WIDTH // 2

        round_text = self.font.render(f"Round: {self.round_number}", True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20, 10)

        remaining_lives = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        lives_rect = remaining_lives.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20, 10)

        # Draw text
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(remaining_lives, lives_rect)

        pygame.draw.line(display_surface, WHITE, (0, 50), (WINDOW_WIDTH, 50), 4)
        pygame.draw.line(display_surface, WHITE, (0, MOVEMENT_THRESHOLD), (WINDOW_WIDTH, MOVEMENT_THRESHOLD), 2)

    def shift_aliens(self):
        """Shift the aliens down and change direction"""
        # Determine if the aliens have hit the edge of the screen
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.right >= WINDOW_WIDTH or alien.rect.left <= 0:
                shift = True

        # Shift every alien down and change direction, and check for breach
        if shift:
            breach = False
            for alien in (self.alien_group.sprites()):
                # Shift down
                alien.rect.y += 6 * self.round_number

                # Reverse alien direction and bump the aliens off the edge
                # This is so that the shift_aliens() method is only called once
                alien.direction *= -1
                alien.rect.x += 5 * alien.direction  # alien.velocity * alien.direction also works

                # Check for breach
                if alien.rect.bottom >= MOVEMENT_THRESHOLD:
                    breach = True

            # Aliens breached the line
            if breach:
                # Play breach sound
                self.breach_sound.play()

                # Remove a life from the player
                self.player.lives -= 1

                # Reset the player's position
                self.player.rect.centerx = WINDOW_WIDTH // 2
                self.player.bottom = WINDOW_HEIGHT - 10

                self.check_game_status("Aliens breached the line!", "Press 'Enter to continue")

    def check_collisions(self):
        """Check for collisions"""
        if pygame.sprite.groupcollide(self.bullet_group, self.alien_group, True, True):
            # Play sound
            self.alien_hit_sound.play()

            # Increase score
            self.score += 10

        if pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True):
            # Play sound
            self.player_hit_sound.play()

            # Remove a life from the player
            self.player.lives -= 1

            # Reset the player's position
            self.player.reset()

            self.check_game_status("You were hit!", "Press 'Enter' to continue")

    def check_round_completion(self):
        """Check if the round is complete"""
        if len(self.alien_group) == 0:
            self.score += 1000 * self.round_number
            self.round_number += 1

            # Check if the score is higher than the high score
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

            self.start_new_round()

    def start_new_round(self):
        """Start a new round of aliens"""
        # Create a grid of aliens. 10 columns, 5 rows
        for row in range(10):
            for column in range(5):
                alien = Alien(64 + (row * 64), 64 + (column * 64), self.round_number, self.alien_bullet_group)
                self.alien_group.add(alien)

        # Pause the game and promt the user to start
        self.pause_game("Space Invaders round: " + str(self.round_number) + ",  High score: " + str(self.high_score), "Press 'Enter' to start")
        self.new_round_sound.play()

    def check_game_status(self, main_text, sub_text):
        """Check to see the status of the game and how the player died"""

        # Empty all bullet_group
        self.alien_bullet_group.empty()
        self.bullet_group.empty()
        self.player.reset()
        for alien in self.alien_group:
            alien.reset()

        # Check if the game is over or a simple round reset
        if self.player.lives <= 0:
            self.reset_game()
        else:
            self.pause_game(main_text, sub_text)
            # self.start_new_round()

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        # Set colours
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Pause game text
        pause_text = self.font.render(main_text, True, WHITE)
        pause_rect = pause_text.get_rect()
        pause_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Sub text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

        # Blit the text
        self.display_surface.fill(BLACK)
        self.display_surface.blit(pause_text, pause_rect)
        self.display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        # Pause music
        self.new_round_sound.stop()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check for keypress
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False

    def reset_game(self):
        """Reset the game"""
        self.pause_game("Game Over! Final score: " + str(self.score), "Press 'Enter' to play again")

        # Reset the game values
        self.score = STARTING_SCORE
        self.round_number = STARTING_ROUND_NUMBER
        self.player.lives = STARTING_LIVES

        # Empty all sprite groups
        self.alien_group.empty()
        self.bullet_group.empty()
        self.alien_bullet_group.empty()

        # Start a new round
        self.start_new_round()

    def read_high_score(self):
        """Read the high score from a file"""
        # Determine the location of the high score file
        if hasattr(sys, '_MEIPASS'):
            high_score_file = os.path.join(sys._MEIPASS, "high_score.txt")
        else:
            high_score_file = "high_score.txt"

        # Read the high score from the file
        with open(high_score_file, "r") as file:
            saved_high_score = file.read()
            return int(saved_high_score)

    def save_high_score(self):
        """Save the high score to a file"""
        # Determine the location of the high score file
        if hasattr(sys, '_MEIPASS'):
            high_score_file = os.path.join(sys._MEIPASS, "high_score.txt")
        else:
            high_score_file = "high_score.txt"

        # Save the high score to the file
        with open(high_score_file, "w") as file:
            file.write(str(self.high_score))