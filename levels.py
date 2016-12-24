import constants as constants
import enemies as enemies
from spritesheet_functions import SpriteSheet
import pygame


class Level(pygame.sprite.Sprite):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    enemy_list = None
    list_of_stewies = []
    cur_enemy = 0
    bg1 = ""
    bg2 = ""

    background = None

    # How far this world has been scrolled left/right
    world_shift = 0

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving enemies
            collide with the player. """

        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.bg1 = pygame.image.load("images/bgk.png").convert()
        self.bg2 = pygame.image.load("images/bg2.png").convert()

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level.

          Arguments:
           screen (pygame.Surface): surface.

        """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.GREEN)
        screen.blit(self.background, (self.world_shift // 5, 0))

        # Draw all the sprite lists that we have
        self.enemy_list.draw(screen)

        if self.player.attack_type == "spirit_bomb":
            screen.blit(self.player.gk_aura, (self.player.rect.x-65, self.player.rect.y-47))
            screen.blit(self.player.gk_bomb, (self.player.rect.x-self.player.bomb_x_coord,
                                              self.player.rect.y-self.player.bomb_y_coord))

            bomb_rect = self.player.gk_bomb.get_rect()
            bomb_rect.x = self.player.rect.x-self.player.bomb_x_coord
            bomb_rect.y = self.player.rect.y-self.player.bomb_y_coord

            hits = pygame.Rect.colliderect(bomb_rect, self.list_of_stewies[self.cur_enemy].rect)
            if hits == 1 and self.player.sp_index > 8:
                img = self.player.stew_dead
                en = self.list_of_stewies[self.cur_enemy]
                en.dead = True
                if en.dir == "L":
                    en.image = img
                else:
                    en.image = pygame.transform.flip(img, True, False)

                en.change_x = 0
                en.change_y = 0
                en.rect.y = 529

        bar = SpriteSheet("images/health_bar.png").get_image(0, 0, 790, 127)
        screen.blit(bar, (0, 0))
        myfont2 = pygame.font.SysFont("monospace", 25, bold=True)
        label2 = myfont2.render("Goku SSJ4", 1, constants.BLACK)
        screen.blit(label2, (120, 78))

        if self.player.health <= 0:
            self.player.health = 0
            self.player.health_br_thickness = -1
            myfont = pygame.font.SysFont("monospace", 30, bold=True)
            label = myfont.render("Game Over! Press p to play again", 1, constants.RED)
            screen.blit(label, (125, 35))

        pygame.draw.rect(screen, self.player.health_color, [120, 32, self.player.health,
                                40], self.player.health_br_thickness)

        if self.player.health < 290:
            self.player.health_color = constants.YELLOW

        if self.player.health < 140:
            self.player.health_color = constants.RED

        if self.player.attack_type == "spirit_bomb":
            self.background = self.bg2
        else:
            self.background = self.bg1

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything:

        Arguments:
          shift_x (int): amount to shift along x axis.
        """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("images/bgk.png").convert()
        self.background.set_colorkey(constants.WHITE)

        # first enemy in level moving along x axis
        block = enemies.MovingEnemy(enemies.STEWIE, "images/stew.png")
        block.rect.x = 420
        block.rect.y = 517
        block.boundary_left = 370
        block.boundary_right = 850
        block.change_x = 7
        block.player = self.player
        block.level = self
        self.list_of_stewies.append(block)
        self.enemy_list.add(self.list_of_stewies[self.cur_enemy])

        # 9 enemies moving up and down
        x_coord = 1400
        speed = 8

        for counter in range(1, 10):
            block1 = enemies.MovingEnemy(enemies.STEWIE, "images/stew.png")
            block1.rect.x = x_coord
            block1.rect.y = 80
            block1.boundary_top = 80
            block1.boundary_bottom = 585
            block1.change_y = speed
            block1.dir = "L"
            block1.image = pygame.transform.flip(block1.image, True, False)
            block1.player = self.player
            block1.level = self
            self.list_of_stewies.append(block1)
            speed *= 1.5
            x_coord += 300
