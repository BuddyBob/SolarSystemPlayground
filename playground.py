import pygame
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1600, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth Orbiting Sun")

# Colors
YELLOW = (201, 175, 58)
BLACK = (25, 25, 25)
BLUE = (40, 70, 237)

# Clock
FPS = 60
clock = pygame.time.Clock()
TS = 60 * 60  # one day
TIME_SIMULATION = 0

#Trail
TRAIL_LENGTH = 100
trail = []

# Constants
G = 6.67430e-11  # m^3 kg^-1 s^-2
SUN_MASS = 1.989e30  # unit of kg
EARTH_MASS = 5.972e24  # unit of kg
DISTANCE_FROM_SUN_M = 1.4959787e11  # unit of meters because all the physics equations use meters

# Convert to pixels for display
# from earth to the sun each pixxel is 249,329,783 meters
METERS_PER_PIXEL = DISTANCE_FROM_SUN_M / 600

# Sun Earth dimensions are not accurate because then the earth would be too small Ratio is no where close either
SUN_RADIUS = 50
EARTH_RADIUS = 10

# Sun position
sun_x = WIDTH // 2
sun_y = HEIGHT // 2

# Intiial Earth position and velocity (not the same all around Earth orbits in an elipse)
earth_x = 147.1e9  # Perihelion distance 
earth_y = 0

# Initial velocity at perihelion
initial_vy = 30290  # editable
earth_vx = 0
earth_vy = initial_vy  # use editable value

# Editable gravitational constants and masses
editable_G = G
editable_SUN_MASS = SUN_MASS
editable_EARTH_MASS = EARTH_MASS

running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE]
        ):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            earth_x = 147.1e9
            earth_y = 0
            earth_vx = 0
            earth_vy = initial_vy
            # Reset editable values
            editable_G = G
            editable_SUN_MASS = SUN_MASS
            editable_EARTH_MASS = EARTH_MASS
            trail.clear()
            TIME_SIMULATION = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                TS += 60
            if event.key == pygame.K_DOWN:
                TS = max(60, TS - 60)
            if event.key == pygame.K_RIGHT:
                initial_vy += 100
            if event.key == pygame.K_LEFT:
                initial_vy -= 100
            if event.key == pygame.K_r:
                earth_x = 147.1e9
                earth_y = 0
                earth_vx = 0
                earth_vy = initial_vy
                trail.clear()
                TIME_SIMULATION = 0
            if event.key == pygame.K_z:
                editable_G *= 1.1
            if event.key == pygame.K_x:
                editable_G *= 0.9
            if event.key == pygame.K_c:
                editable_SUN_MASS *= 1.1
            if event.key == pygame.K_v:
                editable_SUN_MASS *= 0.9
            if event.key == pygame.K_b:
                editable_EARTH_MASS *= 1.1
            if event.key == pygame.K_n:
                editable_EARTH_MASS *= 0.9

    # Vector from Earth to Sun
    dx = -earth_x
    dy = -earth_y
    distance = math.sqrt(dx**2 + dy**2)


    # MOVEMENT VARIABLES

    # Equation used F = G * (m1 * m2) / r^2
    force = editable_G * editable_SUN_MASS * editable_EARTH_MASS / distance**2
    # Equation used a = F / m
    acceleration = force / editable_EARTH_MASS


    ax = acceleration * (dx / distance)
    ay = acceleration * (dy / distance)


    """
    WHY MULTIPLY BY TS?
    equation:
    s = ut + (1/2)at^2
    where:
    s = displacement
    u = initial velocity
    a = acceleration
    t = time step
    """


    # Update velocity
    earth_vx += ax * TS
    earth_vy += ay * TS

    # Update position
    earth_x += earth_vx * TS
    earth_y += earth_vy * TS

    TIME_SIMULATION += TS

    # Convert to pixels for display
    earth_x_px = int(sun_x + earth_x / METERS_PER_PIXEL)
    earth_y_px = int(sun_y + earth_y / METERS_PER_PIXEL)

    # Store trail points
    trail.append((earth_x_px, earth_y_px))
    if len(trail) > TRAIL_LENGTH:
        trail.pop(0)

    # Display data as if this were a real simulation
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 1)
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(
        f"Earth Position: ({earth_x:.2e}, {earth_y:.2e}) m", True, (255, 255, 255)
    )
    screen.blit(text, (10, 10))
    text = font.render(
        f"Earth Velocity: ({earth_vx:.2e}, {earth_vy:.2e}) m/s", True, (255, 255, 255)
    )
    screen.blit(text, (10, 40))
    text = font.render(
        f"Distance from Sun: {distance:.2e} m", True, (255, 255, 255)
    )
    screen.blit(text, (10, 70))
    text = font.render(
        f"Gravitational Force: {force:.2e} N", True, (255, 255, 255)
    )
    screen.blit(text, (10, 100))
    text = font.render(
        f"Acceleration: ({ax:.2e}, {ay:.2e}) m/s^2", True, (255, 255, 255)
    )
    screen.blit(text, (10, 130))
    
    # Current time changes as earth moves
    decade = int(TIME_SIMULATION // (60 * 60 * 24 * 10))
    year = int(TIME_SIMULATION // (60 * 60 * 24 * 365))
    days = int(TIME_SIMULATION // (60 * 60 * 24))
    hours = int((TIME_SIMULATION % (60 * 60 * 24)) // (60 * 60))
    time_display = f"Sim Time: {year}y {days}d {hours}hs"
    font = pygame.font.SysFont("Arial", 20)
    text_surface = font.render(time_display, True, (255, 255, 255))
    screen.blit(text_surface, (10, 160))

    # Extra data about controls and editable vars
    edit1 = font.render(f"[←][→] Earth Initial VY: {initial_vy} m/s", True, (180, 180, 255))
    edit2 = font.render(f"[↑][↓] Time Step (TS): {TS} s", True, (180, 180, 255))
    edit3 = font.render(f"[R] Reset Simulation   [SPACE] Hard Reset", True, (180, 180, 255))
    edit4 = font.render(f"[Z+][X-] Sun Gravity: {editable_G:.2e}", True, (180, 180, 255))
    edit5 = font.render(f"[C+][V-] Sun Mass: {editable_SUN_MASS:.2e} kg", True, (180, 180, 255))
    edit6 = font.render(f"[B+][N-] Earth Mass: {editable_EARTH_MASS:.2e} kg", True, (180, 180, 255))
    screen.blit(edit1, (10, 190))
    screen.blit(edit2, (10, 220))
    screen.blit(edit3, (10, 250))
    screen.blit(edit4, (10, 280))
    screen.blit(edit5, (10, 310))
    screen.blit(edit6, (10, 340))

    # Draw sun and earth
    for point in trail:
        pygame.draw.circle(screen, (100, 100, 255), point, 2)

    pygame.draw.circle(screen, YELLOW, (sun_x, sun_y), SUN_RADIUS)
    pygame.draw.circle(screen, BLUE, (earth_x_px, earth_y_px), EARTH_RADIUS)

    pygame.display.flip()

pygame.quit()
