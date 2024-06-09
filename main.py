import pygame

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 3

# Colors
BLACK = (0, 0, 0)
SAND_COLOR = (194, 178, 128)

# Create a 2D array to represent the grid
grid_width = WIDTH // GRID_SIZE
grid_height = HEIGHT // GRID_SIZE
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# Create a 2D array to represent velocities
velocities = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

def add_sand(x, y):
    if 0 <= x < grid_width and 0 <= y < grid_height:
        grid[y][x] = 1
        velocities[y][x] = 1 

def update_sand():
    for y in range(grid_height - 2, -1, -1):
        for x in range(grid_width):
            if grid[y][x] == 1:
                new_y = y
                new_x = x
                # Find new location
                if y + velocities[y][x] < grid_height and grid[y + velocities[y][x]][x] == 0:
                    new_y = y + velocities[y][x]
                elif x > 0 and y + velocities[y][x] < grid_height and grid[y + velocities[y][x]][x - 1] == 0:
                    new_x = x - 1
                    new_y = y + velocities[y][x]
                elif x < grid_width - 1 and y + velocities[y][x] < grid_height and grid[y + velocities[y][x]][x + 1] == 0:
                    new_x = x + 1
                    new_y = y + velocities[y][x]

                # Apply gravity
                if new_y != y or new_x != x:
                    grid[y][x] = 0
                    grid[new_y][new_x] = 1
                    velocities[new_y][new_x] = velocities[y][x] + 1
                    velocities[y][x] = 0
                else:
                    # If the sand cannot move, stop its velocity
                    velocities[y][x] = 0

def draw_grid(screen):
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, SAND_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Sand Falling Simulator")

    clock = pygame.time.Clock()

    running = True
    mouse_hovering = False

    while running:
        mouse_hovering = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                if 0 <= mouse_x < WIDTH and 0 <= mouse_y < HEIGHT:
                    mouse_hovering = True

        # Add sand at mouse location if hovering
        if mouse_hovering:
            grid_x = mouse_x // GRID_SIZE
            grid_y = mouse_y // GRID_SIZE
            add_sand(grid_x, grid_y)

        # Update sand particles
        update_sand()

        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
