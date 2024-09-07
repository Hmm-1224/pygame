import pygame
import random
import sys
import os
from CoinKeyGemGate import Coin, Key, Gate, Gem
from maze import Maze
from explosion import GemExplosion, KeyExplosion, DestinationExplosion, CoinExplosion, WallExplosion
from ParticleEffect import ParticleEffect
from playerDestination import Player, Destination
# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CELL_SIZE = 40
GAME_DURATION_SEC = 300  
INCREMENT_INTERVAL = 15000  
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
FPS = 30

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
clock = pygame.time.Clock()
WIDTH, HEIGHT = screen.get_size()
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
particle_effects = pygame.sprite.Group()

# Load background music to play it in loop
pygame.mixer.music.load('spygame/soundtrack.mp3')  # Adjust the file name and path as needed
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.07)

coin_collect_sound = pygame.mixer.Sound('cstt.wav')
key_collect_sound = pygame.mixer.Sound('kstt.wav')
gem_collect_sound = pygame.mixer.Sound('gstt.wav')
game_over_sound = pygame.mixer.Sound('gameover.wav')
won_sound = pygame.mixer.Sound('won.wav')

# Set the volume for the sound effects
coin_collect_sound.set_volume(1)  
key_collect_sound.set_volume(1)  
gem_collect_sound.set_volume(1)
game_over_sound.set_volume(1)
won_sound.set_volume(1)

HIGH_SCORE_FILE = 'player_scores.txt'

def read_high_scores():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            scores = [line.strip().split(",") for line in f.readlines()]
            scores = [(name, int(score)) for name, score in scores]
            scores.sort(key=lambda x: x[1], reverse=True)
            return scores[:3]
    except FileNotFoundError:
        return []

def write_high_score(name, new_score):
    with open(HIGH_SCORE_FILE, 'a') as f:
        f.write(f"{name},{new_score}\n")

def get_player_name(): 
    prompt_font = pygame.font.Font(None, 80)  
    input_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 40, 400, 80)
    submit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 60) 
    color_inactive = pygame.Color('darkblue') 
    color_active = pygame.Color('green') 
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 60)
    submit_color_inactive = pygame.Color('blue') 
    submit_color_active = pygame.Color('green')  
    submit_color = submit_color_inactive
    clock = pygame.time.Clock()

    # Load and scale background image
    background = pygame.image.load('maze.png').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                    color = color_active if active else color_inactive
                else:
                    active = False
                    color = color_inactive

                # Check if submit button is clicked
                if submit_button.collidepoint(event.pos) and text:
                    return text  # Return the entered name when submit button is clicked

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text:
                            return text  # Return the entered name when Enter is pressed
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Draw background
        screen.blit(background, (0, 0))

        # Draw prompt text
        prompt_text = prompt_font.render("ENTER YOUR NAME", True, WHITE)
        prompt_x = WIDTH // 2 - prompt_text.get_width() / 2
        prompt_y = HEIGHT // 2 - 120  # Increase distance from input box
        screen.blit(prompt_text, (prompt_x, prompt_y))

        # Draw input box
        txt_surface = font.render(text, True, color)
        width = max(520, txt_surface.get_width() + 10)
        input_box.x = (WIDTH // 2) - (width // 2)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 25))  # Adjusted vertical alignment
        pygame.draw.rect(screen, color, input_box, 10)

        # Draw submit button
        mouse_pos = pygame.mouse.get_pos()
        if submit_button.collidepoint(mouse_pos):
            submit_color = submit_color_active
        else:
            submit_color = submit_color_inactive

        pygame.draw.rect(screen, submit_color, submit_button)
        submit_text = font.render("Submit", True, WHITE)
        submit_text_rect = submit_text.get_rect(center=submit_button.center)
        screen.blit(submit_text, submit_text_rect)

        pygame.display.flip()
        clock.tick(30
                )
def draw_start_menu():
    # Load and scale background image
    start_menu_bg = pygame.image.load('start_screen.png').convert()
    start_menu_bg = pygame.transform.scale(start_menu_bg, (WIDTH, HEIGHT))
    screen.blit(start_menu_bg, (0, 0))
    
    font = pygame.font.SysFont('arial', 40)
    large_font = pygame.font.SysFont('arial', 60)  # Larger font for titles and messages
    
    box_padding = 10
    vertical_spacing = 50
    level_block_width = 200
    level_block_height = 60

    title = font.render('Maze Game', True, WHITE)
    start_button = font.render('Press SPACE to start', True, WHITE)
    exit_button = font.render('Press ESC to exit', True, WHITE)

    start_y = HEIGHT / 2 - title.get_height() / 2
    start_y += 150
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, start_y))
    start_y += vertical_spacing
    
    # Render lives text
    lives_surface = font.render(f"Lives: {lives}", True, WHITE)
    lives_rect = lives_surface.get_rect(topleft=(20, 20))
    screen.blit(lives_surface, lives_rect)

    # Define blocks for each level
    levels = ['Level 1', 'Level 2', 'Level 3']
    level_rects = []
    
    for i, level in enumerate(levels):
        box_x = WIDTH / 2 - level_block_width / 2
        box_y = start_y + i * (level_block_height + box_padding)
        pygame.draw.rect(screen, BLACK, (box_x, box_y, level_block_width, level_block_height))
        level_text = font.render(level, True, WHITE)
        screen.blit(level_text, (WIDTH / 2 - level_text.get_width() / 2, box_y + (level_block_height - level_text.get_height()) / 2))
        level_rects.append(pygame.Rect(box_x, box_y, level_block_width, level_block_height))

    # Draw start and exit buttons
    screen.blit(start_button, (WIDTH / 2 - start_button.get_width() / 2, start_y + len(levels) * (level_block_height + box_padding) + vertical_spacing))
    screen.blit(exit_button, (WIDTH / 2 - exit_button.get_width() / 2, start_y + len(levels) * (level_block_height + box_padding) + vertical_spacing * 2))

    pygame.display.flip()

    return level_rects  # Return rectangles for level buttons

def show_message(message, button_text):
    font = pygame.font.SysFont('arial', 40)
    large_font = pygame.font.SysFont('arial', 60)

    # Prepare the message screen
    screen.fill(BLACK)

    # Draw background
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(WHITE)
    screen.blit(background, (0, 0))

    # Render the message
    message_surface = large_font.render(message, True, BLACK)
    button_surface = font.render(button_text, True, BLACK)
    message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    button_rect = button_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

    # Draw the button background box
    box_padding = 10
    box_width = button_surface.get_width() + 2 * box_padding
    box_height = button_surface.get_height() + 2 * box_padding
    box_x = button_rect.centerx - box_width / 2
    box_y = button_rect.centery - box_height / 2

    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))
    screen.blit(message_surface, message_rect)
    screen.blit(button_surface, (button_rect.x + box_padding, button_rect.y + box_padding))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Game over screen
def draw_game_over(score):
    # Load and scale background image
    end_menu_bg = pygame.image.load('endgame.png').convert()
    end_menu_bg = pygame.transform.scale(end_menu_bg, (WIDTH, HEIGHT))
    screen.blit(end_menu_bg, (0, 0))

    # Initialize font
    font = pygame.font.SysFont('arial', 40)

    # Define text and box dimensions
    box_padding = 10
    vertical_spacing = 80

    # Create text surfaces
    score_text = font.render('Score: ' + str(score), True, WHITE)
    play_again_text = font.render('Press SPACE to play again', True, WHITE)
    top_scores_text = font.render('Press L to see top high scores', True, WHITE)
    main_menu_text = font.render('Press M to Return to Main Menu', True, WHITE)
    exit_text = font.render('Press ESC to Quit', True, WHITE)

    start_y = HEIGHT/2+150

    texts = [score_text, play_again_text, top_scores_text, main_menu_text, exit_text]

    for text in texts:
        # Calculate box dimensions and position
        box_width = text.get_width() + 2 * box_padding
        box_height = text.get_height() + 2 * box_padding
        box_x = WIDTH / 2 - box_width / 2
        box_y = start_y - box_padding
        pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height))
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, start_y))
        start_y += vertical_spacing

key_collected = 0

def select_level(level):
    global CELL_SIZE
    global ROWS, COLS
    maze = Maze()
    if level == 1:
        COLS = (WIDTH // CELL_SIZE) 
        ROWS = (HEIGHT // CELL_SIZE) 
    elif level == 2:
        CELL_SIZE = 35
        COLS = (WIDTH // 35) 
        ROWS = (HEIGHT // 35) 
    elif level == 3:
        CELL_SIZE = 25
        COLS = (WIDTH // 25) 
        ROWS = (HEIGHT // 25) 

def display_high_scores():
    screen.fill(BLACK)
    font = pygame.font.SysFont('arial', 40)
    high_score_title = font.render('Top 3 High Scores:', True, WHITE)
    screen.blit(high_score_title, (WIDTH / 2 - high_score_title.get_width() / 2, HEIGHT / 2 - 150))

    trophy_images = [
        pygame.image.load('gold_trophy.png'),
        pygame.image.load('silver_trophy.png'),
        pygame.image.load('bronze_trophy.png')
    ]
    trophy_images[0] = pygame.transform.scale(trophy_images[0], (40, 40))
    trophy_images[1] = pygame.transform.scale(trophy_images[1], (50, 50))
    trophy_images[2] = pygame.transform.scale(trophy_images[2], (40, 40))

    scores = read_high_scores()

    block_width = 400
    block_height = 50
    block_margin = 20

    y_offset = HEIGHT / 2 - 50

    max_name_width = max(font.render(f'{name}', True, WHITE).get_width() for name, score in scores[:3])
    max_score_width = max(font.render(f'{score}', True, WHITE).get_width() for name, score in scores[:3])

    for i, (name, score) in enumerate(scores[:3]):
        block_x = WIDTH / 2 - block_width / 2
        block_y = y_offset + i * (block_height + block_margin)

        pygame.draw.rect(screen, WHITE, (block_x, block_y, block_width, block_height), 2)

        trophy_image = trophy_images[i]
        screen.blit(trophy_image, (block_x - 50, block_y + block_height / 2 - trophy_image.get_height() / 2))

        rank_text = font.render(f'{i + 1}.', True, WHITE)
        name_text = font.render(name, True, WHITE)
        score_text = font.render(str(score), True, WHITE)

        rank_x = block_x + 20
        name_x = rank_x + rank_text.get_width() + 20
        score_x = block_x + block_width - max_score_width - 20

        screen.blit(rank_text, (rank_x, block_y + block_height / 2 - rank_text.get_height() / 2))
        screen.blit(name_text, (name_x, block_y + block_height / 2 - name_text.get_height() / 2))
        screen.blit(score_text, (score_x, block_y + block_height / 2 - score_text.get_height() / 2))

    return_to_menu_text = font.render('Press M to return to main menu', True, WHITE)
    screen.blit(return_to_menu_text, (WIDTH / 2 - return_to_menu_text.get_width() / 2, HEIGHT / 2 + 200))
    pygame.display.flip()

# Function to check collision with walls
def check_collision(player, maze):
    player_row = player.rect.y // CELL_SIZE
    player_col = player.rect.x // CELL_SIZE
    return maze.grid[player_row][player_col] == 1

# Draw running screen with header
def draw_running_screen(score, lives, minutes, seconds, player, maze, destination):
    screen.fill(WHITE)
    # Draw maze
    maze.draw()

    # Draw player and destination
    screen.blit(player.image, player.rect)
    screen.blit(destination.image, destination.rect)

    # Draw header bar
    header_rect = pygame.Rect(0, 0, WIDTH, 30)
    pygame.draw.rect(screen, BLUE, header_rect)
    
    # Color of score
    score_color = WHITE
    if score > 50:
        score_color = GREEN

    # Color of timer
    timer_color = WHITE
    if minutes == 0 and seconds < 60:
        timer_color = RED

    # Display score, lives, and time on header
    font = pygame.font.SysFont('arial', 20)
    score_text = font.render('Score: ' + str(score), True, score_color)
    lives_text = font.render('Lives: ' + str(lives), True, WHITE)
    time_text = font.render('Time: {:02d}:{:02d}'.format(minutes, seconds), True, timer_color)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH/2 - lives_text.get_width()/2, 10))
    screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    # Update display
    pygame.display.flip()

# Initialize variables
score = 0
lives = 3
INCREMENT_INTERVAL = 12 * 10000  # 10 seconds interval for life increment
GAME_DURATION_SEC = 600  # Total game time in seconds

# Main game loop
running = True
selected_level = 1  # Default level
player_name = get_player_name() 

while running:
    show_start_menu = True
    game_over = False
    score = 0  # Reset score when starting a new game

    # Reset the life increment timer at the start of each game
    life_increment_timer = pygame.time.get_ticks()

    if lives == 0:
        pygame.time.wait(INCREMENT_INTERVAL)
        lives = 1
        show_start_menu = True

    while show_start_menu:
        level_rects = draw_start_menu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                show_start_menu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    show_start_menu = False
                elif event.key == pygame.K_1:
                    selected_level = 1
                elif event.key == pygame.K_2:
                    if key_collected >= 3:
                        selected_level = 2
                    else:
                        show_message("YOU DO NOT HAVE ENOUGH KEYS TO PLAY LEVEL 2", "OK")
                        show_start_menu = True
                elif event.key == pygame.K_3:
                    if key_collected >= 5:
                        selected_level = 3
                    else:
                        show_message("YOU DO NOT HAVE ENOUGH KEYS TO PLAY LEVEL 3", "OK")
                        show_start_menu = True
                elif event.key == pygame.K_SPACE:
                    show_start_menu = False
                    if selected_level:
                        select_level(selected_level)
                        running = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, rect in enumerate(level_rects):
                    if rect.collidepoint(pos):
                        if i == 0:
                            selected_level = 1
                            show_start_menu = False
                        elif i == 1:
                            if key_collected >= 3:
                                selected_level = 2
                                show_start_menu = False
                            else:
                                show_message("YOU DO NOT HAVE ENOUGH KEYS TO PLAY LEVEL 2", "OK")
                        elif i == 2:
                            if key_collected >= 5:
                                selected_level = 3
                                show_start_menu = False
                            else:
                                show_message("YOU DO NOT HAVE ENOUGH KEYS TO PLAY LEVEL 3", "OK")

    if not running:
        break

    maze = Maze()
    player = Player(CELL_SIZE, CELL_SIZE)
    destination = Destination((COLS - 2) * CELL_SIZE, (ROWS - 2) * CELL_SIZE)  # Place the destination at the bottom-right corner
    game_won = False
    start_time = pygame.time.get_ticks()  # Start the game timer

    while not game_over:
        if game_won:
            won_sound.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                draw_game_over(score)
                write_high_score(player_name, score)
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    draw_game_over(score)
                    write_high_score(player_name, score)
                    game_over = True
                elif event.key == pygame.K_m:
                    draw_game_over(score)
                    write_high_score(player_name, score)
                    show_start_menu = True
                    game_over = True
                elif event.key == pygame.K_UP:
                    player.move(0, -CELL_SIZE)
                    if check_collision(player, maze):
                        particle_effects.add(WallExplosion(player.rect.centerx, player.rect.centery))
                        game_over_sound.play()
                        lives -= 1  
                        draw_game_over(score)
                        write_high_score(player_name, score)
                        game_over = True
                    else:
                         score += 1  
                elif event.key == pygame.K_DOWN:
                    player.move(0, CELL_SIZE)
                    if check_collision(player, maze):
                        particle_effects.add(WallExplosion(player.rect.centerx, player.rect.centery))
                        game_over_sound.play()
                        lives -= 1
                        draw_game_over(score)
                        write_high_score(player_name, score)
                        game_over = True
                    else:
                        score += 1
                elif event.key == pygame.K_LEFT:
                    player.move(-CELL_SIZE, 0)
                    if check_collision(player, maze):
                        particle_effects.add(WallExplosion(player.rect.centerx, player.rect.centery))
                        game_over_sound.play()
                        lives -= 1
                        draw_game_over(score)
                        write_high_score(player_name, score)
                        game_over = True
                    else:
                        score += 1
                elif event.key == pygame.K_RIGHT:
                    player.move(CELL_SIZE, 0)
                    if check_collision(player, maze):
                        particle_effects.add(WallExplosion(player.rect.centerx, player.rect.centery))
                        game_over_sound.play()
                        lives -= 1
                        draw_game_over(score)
                        write_high_score(player_name, score)
                        game_over = True
                    else:
                        score += 1

        
        # Check collision with coins
        coin_collisions = pygame.sprite.spritecollide(player, maze.coins, True)  # Detect collisions and remove coins
        for coin in coin_collisions:
            coin_collect_sound.play()
            coin_explosion = CoinExplosion(coin.rect.centerx, coin.rect.centery)
            particle_effects.add(coin_explosion)
            score += 9  # Increase score when collecting a coin

        # Check if player collects keys
        key_collisions = pygame.sprite.spritecollide(player, maze.keys, True)  # Detect collisions and remove keys
        for key in key_collisions:
            key_collect_sound.play()
            key_explosion = KeyExplosion(key.rect.centerx, key.rect.centery)
            particle_effects.add(key_explosion)
            key_collected += 1

        # Gate collision check
        gate_collisions = pygame.sprite.spritecollide(player, maze.gates, False)
        gates_to_remove = []

        for gate in gate_collisions:
            if key_collected > 0:
                key_collect_sound.play()
                key_collected -= 1
                gates_to_remove.append(gate)
            else:
                game_over = True  # End game if player collides with a gate and no keys are available

        for gate in gates_to_remove:
            maze.gates.remove(gate)

        # Check if player collects gems
        gem_collisions = pygame.sprite.spritecollide(player, maze.gems, True)  # Detect collisions and remove gems
        for gem in gem_collisions:
            gem_collect_sound.play()
            gem_explosion = GemExplosion(gem.rect.centerx, gem.rect.centery)
            particle_effects.add(gem_explosion)
            player_row = player.rect.y // CELL_SIZE
            player_col = player.rect.x // CELL_SIZE
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    row = player_row + dr
                    col = player_col + dc
                    if 0 < row < ROWS - 1 and 0 < col < COLS - 1 and maze.grid[row][col] == 1:
                       maze.grid[row][col] = 0

        # Check if player collects keys
        key_collisions = pygame.sprite.spritecollide(player, maze.keys, True)  # Detect collisions and remove keys
        for key in key_collisions:
            key_collect_sound.play()
            key_explosion = KeyExplosion(key.rect.centerx, key.rect.centery)
            particle_effects.add(key_explosion)
            key_collected += 1

        # Gate collision check
        gate_collisions = pygame.sprite.spritecollide(player, maze.gates, False)
        gates_to_remove = []

        for gate in gate_collisions:
           if key_collected > 0:  # Player has a key
               key_collect_sound.play()
               key_collected -= 1
               gates_to_remove.append(gate)  # Add the gate to the list for removal
           else:
               game_over = True  

        # Remove gates that the player has passed through
        for gate in gates_to_remove:
            maze.gates.remove(gate)

        # After collision check, update the display
        pygame.display.flip()

        # Check if player reaches the destination
        if player.rect.colliderect(destination.rect):
            score += 100
            game_won = True
            game_over = True
        if game_won:
            won_sound.play()

        # Timer and life increment logic
        elapsed_time_ms = pygame.time.get_ticks() - start_time
        elapsed_time_sec = elapsed_time_ms // 1000
        remaining_time_sec = max(0, GAME_DURATION_SEC - elapsed_time_sec)
        remaining_minutes = remaining_time_sec // 60
        remaining_seconds = remaining_time_sec % 60

        if lives < 3 and pygame.time.get_ticks() - life_increment_timer >= INCREMENT_INTERVAL:
            lives += 1
            life_increment_timer = pygame.time.get_ticks()

        if remaining_minutes == 0 and remaining_seconds == 0:
            game_over = True

        # Draw the running screen
        draw_running_screen(score, lives, remaining_minutes, remaining_seconds, player, maze, destination)

        particle_effects.update()
        particle_effects.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    draw_game_over(score)
    pygame.display.update()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if lives != 0:
                        game_over = False
                        running = True
                    elif lives == 0:
                        pygame.time.wait(INCREMENT_INTERVAL)
                        lives = 1
                        show_start_menu = True
                elif event.key == pygame.K_m:
                    game_over = False
                    show_start_menu = True
                elif event.key == pygame.K_l:
                    display_high_scores()

pygame.quit()

