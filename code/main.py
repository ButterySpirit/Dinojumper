import random

import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('code/resources/dino.png').convert_alpha()
        player_walk2 = pygame.image.load('code/resources/dinowalk.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('code/resources/dinowalk.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(120, 336))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 336:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 336:
            self.rect.bottom = 336

    def animation_state(self):
        if self.rect.bottom < 336:
            self.image = self.player_jump
        else:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame1 = pygame.image.load('code/resources/flyrecolored.png').convert_alpha()
            fly_frame2 = pygame.image.load('code/resources/flyrecolored2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 300
        elif type == 'spikes':
            spikes_surf = pygame.image.load('code/resources/object 2.png').convert_alpha()
            self.frames = [spikes_surf]
            y_pos = 336

        elif type == 'cactus':
            cactus_surf = pygame.image.load('code/resources/object 1.png')
            self.frames = [cactus_surf]
            y_pos = 335

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def check_high_score(current_score):
    try:
        with open('score.txt', 'r') as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0

    if current_score > high_score:
        with open('score.txt', 'w') as file:
            file.write(str(current_score))
        return current_score
    return high_score

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) // 1000)
    score_surf = test_font.render(f'Score:{current_time}', False, 'Orange')
    score_rect = score_surf.get_rect(center=(400, 50))
    window.blit(score_surf, score_rect)
    return current_time


def high_score():
    hi_score = 0
    current_time = int((pygame.time.get_ticks() - start_time) // 1000)
    if current_time > hi_score:
        hi_score = current_time
    return hi_score


def obstacle_movement(obstacle_list, game_speed):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.rect.x -= game_speed  # Update obstacle's x-coordinate

            if obstacle.rect.bottom==335:
                window.blit(cactus_surf,obstacle.rect)

            elif obstacle.rect.bottom == 336:
                window.blit(spikes_surf, obstacle.rect)
            else:
                window.blit(fly_surf, obstacle.rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.rect.x > -100]
        return obstacle_list
    else:
        return []


game_speed = 5
background_speed=5
def collisons(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 336:
        player_surf = player_jump
    else:
        player_index += 0.2
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]



pygame.init()
window = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Dino :*)')
clock = pygame.time.Clock()
start_time = 0
score = 0
game_active = False
# groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

test_font = pygame.font.Font('code/font/Pixeltype.ttf', 50)
floor1 = pygame.image.load('code/resources/floor.png').convert()
keys = pygame.key.get_pressed()
score_surf = test_font.render('ur moms a hoe', False, 'Orange').convert_alpha()
score_rect = score_surf.get_rect(center=(400, 50))

gameover_dino = pygame.image.load('code/resources/dinowalk.png').convert_alpha()
gameover_dino_scaled = pygame.transform.scale(gameover_dino, (128, 128))
gameover_dino_rect = gameover_dino_scaled.get_rect(center=(400, 200))
gameover_text_instructions = test_font.render('press up arrow to start', False, 'Black').convert_alpha()
gameover_text_instructions_rect = gameover_text_instructions.get_rect(center=(400, 290))
gameover_title = test_font.render('Dino run', False, 'Lime').convert_alpha()
gameover_title_rect = gameover_title.get_rect(center=(400, 50))

background_surf = pygame.image.load('code/resources/dinobackground2.png').convert()  # Convert speeds up blitting
background_rect = background_surf.get_rect(topleft=(0, 0))
# If your background is smaller than the screen, use two side by side
background_surf2 = pygame.image.load('code/resources/dinobackground2.png').convert()
background_rect2 = background_surf2.get_rect(topleft=(background_rect.width, 0))
# Loading the third background
background_surf3 = pygame.image.load('code/resources/dinobackground2.png').convert()
background_rect3 = background_surf3.get_rect(topleft=(background_rect2.width + background_rect2.left, 0))




# obstacles
spikes_surf = pygame.image.load('code/resources/object 2.png').convert_alpha()
spike_rect = spikes_surf.get_rect(midbottom=(600, 336))

cactus_surf = pygame.image.load('code/resources/object 1.png').convert_alpha()
cactus_rect = cactus_surf.get_rect(midbottom=(900, 335))

fly_frame1 = pygame.image.load('code/resources/flyrecolored.png').convert_alpha()
fly_frame2 = pygame.image.load('code/resources/flyrecolored2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]
obstacle_rect_list = []

# player
player_walk1 = pygame.image.load('code/resources/dino.png').convert_alpha()
player_walk2 = pygame.image.load('code/resources/dinowalk.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_surf = player_walk[player_index]
player_jump = pygame.image.load('code/resources/dinowalk.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 336))
player_gravity = 0

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer, 200)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                game_active = True
                spike_rect.left = 800
                start_time = pygame.time.get_ticks()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','spikes','cactus'])))



            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        # Clear the window first
        window.fill('Black')

        # Scroll and redraw the background
        background_rect.x -= background_speed
        background_rect2.x -= background_speed
        if background_rect.right < 0:
            background_rect.left = background_rect2.right
        if background_rect2.right < 0:
            background_rect2.left = background_rect.right
        if background_rect3.right < 0:
            background_rect3.left = background_rect2.right

        window.blit(background_surf, background_rect)
        window.blit(background_surf2, background_rect2)
        window.blit(background_surf3, background_rect3)

        # Draw the floor after the background
        for a in range(0, 13):
            window.blit(floor1, (a * 64, 336))

        # Update the score and display it
        score = display_score()

        # Process player input and update player
        player.update()
        player.draw(window)

        # Update and draw obstacles
        obstacle_group.update()
        obstacle_group.draw(window)

        # Check collisions between the player and obstacles
        game_active = collision_sprite()


    else:  # This is the part of the code where game_active is False

        window.fill('orange')
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 336)
        player_gravity = 0
        window.blit(gameover_dino_scaled, gameover_dino_rect)
        window.blit(gameover_title, gameover_title_rect)
        high_score = check_high_score(score)  # Check and update the high score
        score_message = test_font.render(f'Score: {score}', False, 'Black')
        score_message_rect = score_message.get_rect(center=(400, 300))
        high_score_message = test_font.render(f'High Score: {high_score}', False, 'Black')  # Display high score
        high_score_message_rect = high_score_message.get_rect(center=(400, 350))  # Adjust Y coordinate for spacing
        game_speed = 5
        background_speed = 5

        if score == 0:
            window.blit(gameover_text_instructions, gameover_text_instructions_rect)

            window.blit(high_score_message, high_score_message_rect)  # Blit the high score

        else:
            window.blit(score_message, score_message_rect)
            window.blit(high_score_message, high_score_message_rect)  # Blit the high score

    if score > 0 and score % 10 == 0:
        game_speed += 0.01  # Increase game speed by 0.01 when score is a multiple of 10
        background_speed += 0.01
        print(game_speed)


    pygame.display.update()
    clock.tick(60)
