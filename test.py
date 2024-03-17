import pygame, sys
from setting import *
from random import randint, choice

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('PTG')
clock = pygame.time.Clock()
FONT = pygame.font.Font('PTG/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
BG_music = pygame.mixer.Sound('PTG/audio/music.wav')
BG_music.set_volume(0.1)
BG_music.play(loops = -1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('PTG/resc/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('PTG/resc/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('PTG/resc/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('PTG/audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('PTG/resc/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('PTG/resc/Fly/Fly2.png').convert_alpha()
            self.frame = [fly_1, fly_2]
            y_pos = 200
        else:
            snail_1 = pygame.image.load('PTG/resc/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('PTG/resc/snail/snail2.png').convert_alpha()
            self.frame = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frame[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frame): self.animation_index = 0
        self.image = self.frame[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = FONT.render(f'Score: {current_time}', True, (64,64,64))
    score_rect = score_surf.get_rect(midtop = (400, 25))
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    screen.blit(score_surf, score_rect)
    return current_time 

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Menu Screen
gametitle = FONT.render('PyThonGame', True, 'red')
gametitle = pygame.transform.rotozoom(gametitle,0,2)
gametitle_rect = gametitle.get_rect(center = (400, 80))

game_tutor = FONT.render('Press space to jump', False, (111,196,169))
game_tutor_rect = game_tutor.get_rect(center = (400,300))

# Background
sky_surf = pygame.image.load('PTG/resc/sky.png')
groudn_surf = pygame.image.load('PTG/resc/ground.png')


# Timer
ob_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ob_timer,2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
            if event.type == ob_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(groudn_surf,(0,300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()
    else:
        screen.fill((94,129,162))
        # Game over screen
        score_over = FONT.render(f"Your score: {score}", False, 'black')
        score_over_rect = score_over.get_rect(center = (400,300))
        restart_message = FONT.render("Press space to restart", False, (111,196,169))
        restart_message_rect = restart_message.get_rect(center = (400, 350))
        screen.blit(gametitle, gametitle_rect)
        if score == 0:
            screen.blit(game_tutor, game_tutor_rect)
        else:
            
            screen.blit(score_over, score_over_rect)
            screen.blit(restart_message, restart_message_rect)

    pygame.display.update()
    clock.tick(FPS)