import pygame
import random
from collections import deque
from CoinKeyGemGate import Coin, Key, Gate, Gem
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

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
WIDTH, HEIGHT = screen.get_size()
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))

block_image = pygame.image.load('block.png').convert()  # Load the wall image
block_image = pygame.transform.scale(block_image, (CELL_SIZE, CELL_SIZE))  # Scale to fit cell size

class Maze:
    def __init__(self):
        self.grid = [[1] * COLS for _ in range(ROWS)]  # Initialize maze with walls
        self.coins = pygame.sprite.Group()  # Group to hold coin sprites
        self.keys = pygame.sprite.Group()  # Group for keys
        self.gates = pygame.sprite.Group()  # Group for gates
        self.gems = pygame.sprite.Group()  # Group for gems
        self.generate_maze()

    def generate_maze(self):
        # Recursive Backtracking algorithm to generate maze
        def recursive_backtrack(row, col):
            self.grid[row][col] = 0  # Mark the current cell as empty

            # Define the order in which to explore neighbors randomly
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)

            for dr, dc in directions:
                r, c = row + dr * 2, col + dc * 2
                if 1 <= r < ROWS - 1 and 1 <= c < COLS - 1 and self.grid[r][c] == 1:
                    self.grid[row + dr][col + dc] = 0
                    recursive_backtrack(row + dr * 2, col + dc * 2)

        # Start the maze generation from a random cell inside the boundaries
        start_row = random.randrange(1, ROWS - 1, 2)
        start_col = random.randrange(1, COLS - 1, 2)
        recursive_backtrack(start_row, start_col)

        # Place coins, keys, gates, and gems randomly within the maze boundaries
        self.place_items()

        # Ensure solution path exists
        self.ensure_solution_path()

    def place_items(self):
        # Place coins
        while len(self.coins) < 50:  # Adjust the number of coins as needed
            row = random.randrange(1, ROWS - 1)
            col = random.randrange(1, COLS - 1)
            if self.grid[row][col] == 0:  # Only place coins in empty cells
                self.coins.add(Coin(col * CELL_SIZE, row * CELL_SIZE))

        # Place keys
        while len(self.keys) < 5:  # Adjust the number of keys as needed
            row = random.randrange(1, ROWS - 1)
            col = random.randrange(1, COLS - 1)
            if self.grid[row][col] == 0:  # Only place keys in empty cells
                self.keys.add(Key(col * CELL_SIZE, row * CELL_SIZE))

        # Place gates
        while len(self.gates) < 5:  # Adjust the number of gates as needed
            key_pos = random.choice(list(self.keys))  # Choose a random key position
            # Ensure gates are placed closer to keys
            row = random.randint(max(1, key_pos.rect.y // CELL_SIZE - 5), min(ROWS - 2, key_pos.rect.y // CELL_SIZE + 5))
            col = random.randint(max(1, key_pos.rect.x // CELL_SIZE - 5), min(COLS - 2, key_pos.rect.x // CELL_SIZE + 5))
            if self.grid[row][col] == 0:  # Only place gates in empty cells
                self.gates.add(Gate(col * CELL_SIZE, row * CELL_SIZE))

        # Place gems
        while len(self.gems) < 5:  # Adjust the number of gems as needed
            row = random.randrange(1, ROWS - 1)
            col = random.randrange(1, COLS - 1)
            if self.grid[row][col] == 0:  # Only place gems in empty cells
                self.gems.add(Gem(col * CELL_SIZE, row * CELL_SIZE))

    def bfs(self, start_row, start_col, target_row=None, target_col=None):
        visited = set()
        queue = deque([(start_row, start_col)])
        while queue:
            row, col = queue.popleft()
            if (row, col) == (target_row, target_col) or (target_row is None and target_col is None and (row, col) == (ROWS - 2, COLS - 2)):  # Destination reached
                return True  # Solution path exists
            if (row, col) in visited:
                continue
            visited.add((row, col))
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                r, c = row + dr, col + dc
                if 1 <= r < ROWS - 1 and 1 <= c < COLS - 1 and self.grid[r][c] == 0:
                    queue.append((r, c))
        return False  # No solution path

    def ensure_solution_path(self):
        # Ensure the destination cell is empty
        if self.grid[ROWS - 2][COLS - 2] != 0:
            self.grid[ROWS - 2][COLS - 2] = 0
        if not self.bfs(1, 1):
            # If solution path doesn't exist, clear cells in each direction around the end cell
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    if 1 <= ROWS - 2 + dr < ROWS - 1 and 1 <= COLS - 2 + dc < COLS - 1:
                        self.grid[ROWS - 2 + dr][COLS - 2 + dc] = 0
            # Retry maze generation if necessary
            self.ensure_solution_path()

    def draw(self):
        for row in range(ROWS):
            for col in range(COLS):
                if row == 0 or row == ROWS - 1 or col == 0 or col == COLS - 1:
                    # Draw boundary walls
                    screen.blit(block_image, (col * CELL_SIZE, row * CELL_SIZE))
                elif self.grid[row][col] == 1:
                    # Draw internal walls
                    screen.blit(block_image, (col * CELL_SIZE, row * CELL_SIZE))
                else:
                    pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw coins, keys, gates, and gems
        self.coins.draw(screen)
        self.gates.draw(screen)

        for key in self.keys:
            scaled_key = pygame.transform.scale(key.image, (CELL_SIZE, CELL_SIZE))
            screen.blit(scaled_key, key.rect)

        for gem in self.gems:
            scaled_gem = pygame.transform.scale(gem.image, (CELL_SIZE, CELL_SIZE))
            screen.blit(scaled_gem, gem.rect)

