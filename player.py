"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""

import constants as constants
from enemies import MovingEnemy
from spritesheet_functions import SpriteSheet
import pygame

class Player(pygame.sprite.Sprite):
    """ Player class. Handles what the player can do and collisions. """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []

    kame_frames_r = []
    bomb_frames = []
    hit_img = ""
    dying_frames = []
    gk_aura = ""
    gk_bomb = ""

    # What direction is the player facing?
    direction = "R"
    attack_type = " "
    clock = pygame.time.Clock()

    level = None
    index = 0
    health = 583
    health_br_thickness = 0
    health_color = constants.GREEN1
    dying_fr_index = 0
    checkpoint = 1350
    sp_index = 0
    bomb_x_coord = 165
    bomb_y_coord = 400
    stew_dead = ""

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("images/walk.png")

        # Load all the right facing images into a list
        image = sprite_sheet.get_image(801, 129, 59, 85)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(869, 128, 49, 86)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(931, 127, 44, 87)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(989, 128, 54, 86)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(1054, 128, 47, 86)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(1115, 127, 43, 87)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(801, 129, 59, 85)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(869, 128, 49, 86)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(931, 127, 44, 87)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(989, 128, 54, 86)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(1054, 128, 47, 86)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(1115, 127, 43, 87)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # attack right images
        image = sprite_sheet.get_image(7, 517, 72, 91)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(91, 513, 61, 95)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(160, 516, 63, 92)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(229, 514, 61, 94)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(298, 516, 56, 92)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(364, 791, 85, 84)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(456, 790, 87, 85)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(701, 30, 130, 85)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(701, 30, 275, 85)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(701, 30, 450, 85)
        self.kame_frames_r.append(image)
        image = sprite_sheet.get_image(701, 30, 564, 85)
        self.kame_frames_r.append(image)

        # dying to right images
        image1 = sprite_sheet.get_image(640, 795, 68, 80)
        self.dying_frames.append(image1)
        image = sprite_sheet.get_image(715, 789, 59, 86)
        self.dying_frames.append(image)
        image = sprite_sheet.get_image(791, 811, 71, 64)
        self.dying_frames.append(image)
        image = sprite_sheet.get_image(871, 831, 83, 44)
        self.dying_frames.append(image)
        image = sprite_sheet.get_image(962, 845, 91, 30)
        self.dying_frames.append(image)

        # player gets hit image
        self.hit_img = image1

        # spirit bomb attack
        img1 = sprite_sheet.get_image(7, 790, 63, 85)
        self.bomb_frames.append(img1)
        self.bomb_frames.append(img1)
        img1 = sprite_sheet.get_image(82, 777, 52, 98)
        self.bomb_frames.append(img1)
        self.bomb_frames.append(img1)
        img1 = sprite_sheet.get_image(142, 777, 60, 98)
        self.bomb_frames.append(img1)
        self.bomb_frames.append(img1)
        img1 = sprite_sheet.get_image(211, 777, 54, 98)
        self.bomb_frames.append(img1)
        self.bomb_frames.append(img1)
        img1 = sprite_sheet.get_image(270, 790, 87, 85)
        self.bomb_frames.append(img1)
        self.bomb_frames.append(img1)
        img1 = sprite_sheet.get_image(364, 791, 85, 84)
        self.bomb_frames.append(img1)
        img1 = sprite_sheet.get_image(456, 790, 87, 85)
        self.bomb_frames.append(img1)

        self.gk_aura = pygame.image.load("images/aura2.png").convert_alpha()
        self.gk_bomb = pygame.image.load("images/spirit2.png").convert_alpha()

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        self.stew_dead = SpriteSheet("images/stew_dead.png").get_image(0, 0, 80, 68)

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        pos = self.rect.x + self.level.world_shift
        player_pos = self.rect.x - self.level.world_shift

        if player_pos > self.checkpoint:
            self.level.enemy_list.remove(self.level.list_of_stewies[self.level.cur_enemy])
            if self.level.cur_enemy < len(self.level.list_of_stewies)-1:
                self.level.cur_enemy += 1
                self.level.enemy_list.add(self.level.list_of_stewies[self.level.cur_enemy])

                self.checkpoint = (self.level.list_of_stewies[self.level.cur_enemy].rect.x
                                   - self.level.world_shift) + 520

        if self.health != 0:

            if self.direction == "R":
                frame = (pos // 30) % len(self.walking_frames_r)

                self.image = self.walking_frames_r[frame]

                # kamehameha attack
                if self.attack_type == "kame":
                    if self.index < 20:
                        self.clock.tick(7)
                        if self.index > 10:
                            self.image = self.kame_frames_r[10]
                            self.rect.width = self.image.get_width()

                        else:
                            self.image = self.kame_frames_r[self.index]
                            self.rect.width = self.image.get_width()

                        self.index += 1

                # spirit bomb attack
                if self.attack_type == "spirit_bomb":

                    if self.rect.y > 500:
                        self.rect.y = 500
                    if self.sp_index < 35:
                        if self.sp_index > 7:
                            self.bomb_x_coord -= 33
                        if 19 > self.sp_index > 8:
                            if self.rect.y < 420:
                                self.bomb_y_coord -= 28
                            else:
                                self.bomb_y_coord -= 13

                        if self.sp_index > 11:
                            self.clock.tick(12)
                            self.image = self.bomb_frames[11]
                            self.change_y = 0
                        else:
                            self.clock.tick(12)
                            self.image = self.bomb_frames[self.sp_index]
                            self.change_y = 0

                        self.sp_index += 1

            else:
                frame = (pos // 30) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)

        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit

            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

            elif self.index > 6:
                img = self.stew_dead
                block.dead = True
                if block.dir == "L":
                    block.image = img
                else:
                    block.image = pygame.transform.flip(img, True, False)

                block.change_x = 0
                block.change_y = 0
                block.rect.y = 529

            if self.index == 0 and block.dead is False:
                if self.health != 0:
                    if self.direction == "R":
                        self.image = self.hit_img
                    else:
                        self.image = pygame.transform.flip(self.hit_img, True, False)

                    self.health -= 15

        if self.health == 0 and self.dying_fr_index < 5:
            if self.direction == "R":
                my_img = self.dying_frames[self.dying_fr_index]
                add_to_x = -25
            else:
                my_img = pygame.transform.flip(self.dying_frames[self.dying_fr_index], True, False)
                add_to_x = 25

            self.image = my_img
            self.rect.height = self.image.get_height()
            self.clock.tick(7)
            self.rect.x += add_to_x
            self.dying_fr_index += 1

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingEnemy):
                self.rect.x += block.change_x

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .8

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -17

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -5.5
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 5.5
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
