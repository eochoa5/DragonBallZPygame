"""
Module for managing enemies.
"""

import constants as constants
from spritesheet_functions import SpriteSheet
import pygame
import random

#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

STEWIE = (0, 0, 69, 80)


class Enemy(pygame.sprite.Sprite):
    """ Enemy class. Only Enemy is Stewie. """

    def __init__(self, sprite_sheet_data, file_name):
        """ Enemy constructor. Assumes constructed with user passing in
            a tuple of 4 numbers like what's defined at the top of this
            code and image name.

            Arguments:
             sprite_sheet_data (tuple): tuple of 4 numbers to access sprite.
             file_name (str): name of file.
            """
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet(file_name)
        # Grab the image for this enemy
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()


class MovingEnemy(Enemy):
    """ Moving Enemy. Can move up/down, left/right, diagonally. """
    change_x = 0
    change_y = 0
    dead = False
    dir = "R"
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    level = None
    player = None
    has_played = False

    def update(self):
        """ Move the enemy, Handle collisions, play sounds."""

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and self.player.attack_type != "kame" and self.dead is False\
                and self.player.attack_type != "spirit_bomb":
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
            # If we are moving right, set our right side
            # to the left side of the item we hit

            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

            if self.player.health != 0:
                if self.player.direction == "R":
                    self.player.image = self.player.hit_img
                else:
                    self.player.image = pygame.transform.flip(self.player.hit_img, True, False)

            self.player.health -= 15

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and self.player.attack_type != "kame" and self.dead is False\
                and self.player.attack_type != "spirit_bomb":
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

            if self.player.health != 0 and self.change_y > 0:
                if self.player.direction == "R":
                    self.player.image = self.player.hit_img
                else:
                    self.player.image = pygame.transform.flip(self.player.hit_img, True, False)

                self.player.health -= 15

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        player_pos = self.player.rect.x - self.level.world_shift
        diff = abs(cur_pos - player_pos)

        distance = self.boundary_top + 200
        rand = random.randint(0, 4)

        if rand == 0:
            stewie_sound = pygame.mixer.Sound('sounds/stewie.ogg')
        elif rand == 1:
            stewie_sound = pygame.mixer.Sound('sounds/laugh.ogg')
        elif rand == 2:
            stewie_sound = pygame.mixer.Sound('sounds/money.ogg')
        elif rand == 3:
            stewie_sound = pygame.mixer.Sound('sounds/ftman.ogg')
        else:
            stewie_sound = pygame.mixer.Sound('sounds/minus.ogg')

        if self.rect.y > distance and self.has_played is False and self.dead is False and diff < 250:
            stewie_sound.set_volume(1)
            stewie_sound.play()
            if rand == 1:
                self.player.health -= 100
            self.has_played = True

        if cur_pos < self.boundary_left or cur_pos > self.boundary_right and self.dead is False:
            self.change_x *= -1
            if self.dir == "R":
                self.dir = "L"
            else:
                self.dir = "R"

            if self.change_y == 0 and self.dead is False:
                self.image = pygame.transform.flip(self.image, True, False)
