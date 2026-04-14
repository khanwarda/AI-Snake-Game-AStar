"""
===============================================================================
README: AI Auto-Pilot Snake Game (A* Pathfinding Algorithm)
===============================================================================

Prerequisites & Installation:
-----------------------------
To run this project, you only need pygame.
    $ pip install pygame

AI Logic (A* Pathfinding):
--------------------------
Instead of physical inputs, this version features an Autonomous AI Agent.
1. The AI uses the A* (A-Star) search algorithm to find the optimal path 
   from the snake's head to the food.
2. Heuristic: Manhattan Distance is used to estimate the cost from any node 
   to the target, ensuring fast and efficient path calculation.
3. Obstacle Avoidance: The algorithm treats the game boundaries and the snake's 
   own body as impassable obstacles.
4. Fallback: If no valid path is found (e.g., the snake is trapped), it defaults
   to a safe move to prolong survival.

Controls:
---------
- Arrow Keys: Manual control of the snake.
- Key 'A': Toggle AI Auto-Pilot ON/OFF.
- Key 'SPACE': Restart game after Game Over.
- Key 'ESC': Quit.
===============================================================================
"""

import sys
import random
import heapq
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict

import pygame

# --- Constants & Configuration ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 8  # Normal speed

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __lt__(self, other):
        # Required for heapq comparison (we don't strictly compare points, just costs, 
        # but this prevents errors if costs are equal)
        return (self.x, self.y) < (other.x, other.y)


@dataclass
class GameState:
    snake: List[Point] = field(default_factory=list)
    direction: Direction = Direction.RIGHT
    food: Optional[Point] = None
    score: int = 0
    game_over: bool = False
    ai_mode: bool = False  # Track if AI Auto-pilot is active


class AStarAI:
    """Handles the A* Pathfinding algorithm for the autonomous snake."""
    
    def __init__(self, width: int, height: int, block_size: int):
        self.w = width
        self.h = height
        self.block_size = block_size

    def get_neighbors(self, pt: Point) -> List[Point]:
        """Returns valid adjacent grid points."""
        neighbors = [
            Point(pt.x + self.block_size, pt.y), # Right
            Point(pt.x - self.block_size, pt.y), # Left
            Point(pt.x, pt.y + self.block_size), # Down
            Point(pt.x, pt.y - self.block_size)  # Up
        ]
        return neighbors

    def is_valid(self, pt: Point, snake_body: List[Point]) -> bool:
        """Checks if a point is within bounds and not hitting the snake's body."""
        if pt.x < 0 or pt.x >= self.w or pt.y < 0 or pt.y >= self.h:
            return False
        # The snake's tail will move forward, so it's technically safe to move into the current tail position
        # unless it just ate food, but for simplicity, we treat the whole current body (except tail tip) as an obstacle.
        if pt in snake_body[:-1]:
            return False
        return True

    def manhattan_distance(self, p1: Point, p2: Point) -> int:
        """Heuristic function for A* calculation."""
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def get_next_direction(self, state: GameState) -> Optional[Direction]:
        """Runs the A* algorithm and returns the next immediate direction to take."""
        start = state.snake[0]
        target = state.food

        if not target:
            return None

        # Priority queue for A*: stores tuples of (f_score, Point)
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # Keeps track of where we came from to reconstruct the path
        came_from: Dict[Point, Point] = {}
        
        # Cost from start to current node
        g_score: Dict[Point, int] = {start: 0}
        
        while open_set:
            _, current = heapq.heappop(open_set)

            # If we reached the food, reconstruct path to find the FIRST move
            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                
                if path:
                    next_node = path[-1] # The immediate next step
                    return self._determine_direction(start, next_node)
                return None

            for neighbor in self.get_neighbors(current):
                if not self.is_valid(neighbor, state.snake):
                    continue

                tentative_g_score = g_score[current] + self.block_size

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.manhattan_distance(neighbor, target)
                    heapq.heappush(open_set, (f_score, neighbor))

        # Fallback: If no path to food is found (trapped), just try to make any valid move to stay alive
        for neighbor in self.get_neighbors(start):
             if self.is_valid(neighbor, state.snake):
                 return self._determine_direction(start, neighbor)

        return None # No valid moves, game will end naturally

    def _determine_direction(self, curr: Point, nxt: Point) -> Direction:
        """Converts spatial coordinates into a logical Direction enum."""
        if nxt.x > curr.x: return Direction.RIGHT
        if nxt.x < curr.x: return Direction.LEFT
        if nxt.y > curr.y: return Direction.DOWN
        return Direction.UP


class SnakeGameEngine:
    """Core logic engine for the classic snake game."""
    def __init__(self, width: int, height: int, block_size: int):
        self.w = width
        self.h = height
        self.block_size = block_size
        self.state = GameState()
        self.reset()

    def reset(self) -> None:
        was_ai_on = self.state.ai_mode
        self.state = GameState()
        self.state.ai_mode = was_ai_on # Preserve AI state across restarts
        
        head = Point(self.w // 2, self.h // 2)
        self.state.snake = [
            head,
            Point(head.x - self.block_size, head.y),
            Point(head.x - (2 * self.block_size), head.y)
        ]
        self._place_food()

    def _place_food(self) -> None:
        x = random.randint(0, (self.w - self.block_size) // self.block_size) * self.block_size
        y = random.randint(0, (self.h - self.block_size) // self.block_size) * self.block_size
        self.state.food = Point(x, y)
        if self.state.food in self.state.snake:
            self._place_food()

    def set_direction(self, new_dir: Direction) -> None:
        # Prevent 180-degree turns
        if new_dir == Direction.UP and self.state.direction != Direction.DOWN:
            self.state.direction = new_dir
        elif new_dir == Direction.DOWN and self.state.direction != Direction.UP:
            self.state.direction = new_dir
        elif new_dir == Direction.LEFT and self.state.direction != Direction.RIGHT:
            self.state.direction = new_dir
        elif new_dir == Direction.RIGHT and self.state.direction != Direction.LEFT:
            self.state.direction = new_dir

    def step(self) -> None:
        if self.state.game_over: return

        head = self.state.snake[0]
        x, y = head.x, head.y

        if self.state.direction == Direction.RIGHT: x += self.block_size
        elif self.state.direction == Direction.LEFT: x -= self.block_size
        elif self.state.direction == Direction.DOWN: y += self.block_size
        elif self.state.direction == Direction.UP: y -= self.block_size

        new_head = Point(x, y)

        if self._is_collision(new_head):
            self.state.game_over = True
            return

        self.state.snake.insert(0, new_head)

        if new_head == self.state.food:
            self.state.score += 1
            self._place_food()
        else:
            self.state.snake.pop()

    def _is_collision(self, pt: Point) -> bool:
        if pt.x > self.w - self.block_size or pt.x < 0 or pt.y > self.h - self.block_size or pt.y < 0:
            return True
        if pt in self.state.snake[1:]:
            return True
        return False


class GameRenderer:
    def __init__(self, width: int, height: int):
        pygame.init()
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("AI Auto-Pilot Snake (A* Algorithm)")
        self.font = pygame.font.SysFont("arial", 20)
        self.large_font = pygame.font.SysFont("arial", 50)
        self.clock = pygame.time.Clock()

    def render(self, state: GameState) -> None:
        self.display.fill(BLACK)

        # Draw Snake
        for i, pt in enumerate(state.snake):
            color = BLUE if i == 0 and state.ai_mode else DARK_GREEN
            pygame.draw.rect(self.display, color, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            # Inner details
            inner_color = YELLOW if i == 0 and state.ai_mode else GREEN
            pygame.draw.rect(self.display, inner_color, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        # Draw Food
        if state.food:
            pygame.draw.rect(self.display, RED, pygame.Rect(state.food.x, state.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Draw HUD (Score and Mode)
        score_text = self.font.render(f"Score: {state.score}", True, WHITE)
        mode_text = self.font.render(f"AI Auto-Pilot: {'ON' if state.ai_mode else 'OFF'} (Press 'A')", True, YELLOW if state.ai_mode else WHITE)
        self.display.blit(score_text, [10, 10])
        self.display.blit(mode_text, [10, 35])

        if state.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.display.blit(overlay, (0, 0))
            game_over_text = self.large_font.render("GAME OVER", True, RED)
            self.display.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, WINDOW_HEIGHT//2 - 50))

        pygame.display.flip()

    def tick(self) -> None:
        self.clock.tick(FPS)


def main() -> None:
    engine = SnakeGameEngine(WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)
    renderer = GameRenderer(WINDOW_WIDTH, WINDOW_HEIGHT)
    ai_solver = AStarAI(WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Toggle AI Mode
                if event.key == pygame.K_a:
                    engine.state.ai_mode = not engine.state.ai_mode

                if engine.state.game_over:
                    if event.key == pygame.K_SPACE:
                        engine.reset()
                elif not engine.state.ai_mode:
                    # Manual Controls
                    if event.key == pygame.K_UP: engine.set_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN: engine.set_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT: engine.set_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT: engine.set_direction(Direction.RIGHT)

        # Let AI decide the next move if enabled
        if engine.state.ai_mode and not engine.state.game_over:
            next_ai_dir = ai_solver.get_next_direction(engine.state)
            if next_ai_dir:
                engine.set_direction(next_ai_dir)

        engine.step()
        renderer.render(engine.state)
        renderer.tick()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()