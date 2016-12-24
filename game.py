"""How to play:

x                  - spirit bomb (only while facing right)
space bar          - kamehameha wave (only while facing right)
up arrow key       - jump
right arrow key    - walk to the right
left arrow key     - walk to the left
p                  - start a new game only if dead

"""
import constants as constants
import levels as levels
from player import Player
import pygame
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Dragon Ball Z Game")

    # Create the player
    player = Player()
    current_level = levels.Level_01(player)

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 0
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False
    pygame.mixer.music.load('sounds/opening.mp3')
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(.1)
    attack = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    current_level.shift_world(-120)
    kamehameha = pygame.mixer.Sound('sounds/kame.ogg')
    bomb_sound = pygame.mixer.Sound('sounds/spirit.ogg')
    playing = False
    spirit_attack = False
    playing2 = False

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and attack is False and player.health != 0\
                        and spirit_attack is False:
                    if player.rect.x > 0:
                        player.go_left()
                if event.key == pygame.K_RIGHT and player.health != 0 and attack is False\
                        and spirit_attack is False:
                    player.go_right()
                if event.key == pygame.K_UP and player.health != 0:
                    player.jump()
                if event.key == pygame.K_SPACE and player.direction == "R" and player.health != 0\
                        and spirit_attack is False:
                    attack = True
                if event.key == pygame.K_x and player.health != 0 and player.direction == "R":
                    spirit_attack = True
                if event.key == pygame.K_p and player.health == 0:
                    pygame.quit()
                    os.system('game.py')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
            if event.type == pygame.USEREVENT:
                pygame.mixer.music.play()

        # kamehameha attack
        if attack is True and player.index != 20:
            if playing is False:
                kamehameha.play()
                playing = True
            player.attack_type = "kame"
        else:
            attack = False
            player.rect.width = player.image.get_width()
            kamehameha.stop()
            playing = False
            player.index = 0
            player.attack_type = " "

        # spirit bomb attack
        if spirit_attack is True and player.sp_index != 35:
            if playing2 is False:
                bomb_sound.play()
                playing2 = True
            player.attack_type = "spirit_bomb"
        else:
            spirit_attack = False
            player.sp_index = 0
            player.bomb_x_coord = 165
            player.bomb_y_coord = 400
            if player.attack_type != "kame":
                player.attack_type = " "
            bomb_sound.stop()
            playing2 = False

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        if player.rect.x >= 500 and current_level.world_shift > -28706:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.x <= 120 and current_level.world_shift < 0:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world(diff)
        if player.rect.x < 0:
            player.rect.x = 0

        if player.rect.x > 740:
            player.rect.x = 740

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
