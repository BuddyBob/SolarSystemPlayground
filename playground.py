import pygame
import math

def draw_dynamic_grid(screen, sun_x, sun_y, WIDTH, HEIGHT, current_mpp, GRID_COLOR):
    # --- Draw dynamic grid ---
    grid_spacing_pixels = 100  
    target_spacing = current_mpp * grid_spacing_pixels

    # Get a cute number for the grid spacing
    def cute(x):
        exponent = math.floor(math.log10(x))
        fraction = x / (10**exponent)
        if fraction < 1.5:
            nice_fraction = 1
        elif fraction < 3:
            nice_fraction = 2
        elif fraction < 7:
            nice_fraction = 5
        else:
            nice_fraction = 10
        return nice_fraction * (10**exponent)

    grid_spacing_sim = cute(target_spacing)
    x_min_sim = (0 - sun_x) * current_mpp
    x_max_sim = (WIDTH - sun_x) * current_mpp
    y_min_sim = (0 - sun_y) * current_mpp
    y_max_sim = (HEIGHT - sun_y) * current_mpp

    # Vert
    start_x = math.floor(x_min_sim / grid_spacing_sim) * grid_spacing_sim
    x_val = start_x
    while x_val <= x_max_sim:
        screen_x = sun_x + x_val / current_mpp
        pygame.draw.line(screen, GRID_COLOR, (screen_x, 0), (screen_x, HEIGHT))
        x_val += grid_spacing_sim

    # Horiz
    start_y = math.floor(y_min_sim / grid_spacing_sim) * grid_spacing_sim
    y_val = start_y
    while y_val <= y_max_sim:
        screen_y = sun_y + y_val / current_mpp
        pygame.draw.line(screen, GRID_COLOR, (0, screen_y), (WIDTH, screen_y))
        y_val += grid_spacing_sim

def earth_acceleration(x, y, G, sun_mass):
    # Compute acceleration due to the Sun
    r = math.sqrt(x**2 + y**2)
    ax = - G * sun_mass * x / (r**3)
    ay = - G * sun_mass * y / (r**3)
    return ax, ay

def rocket_acceleration(rx, ry, ex, ey, G, sun_mass, earth_mass):
    # Acceleration due to the Sun 
    r_sun = math.sqrt(rx**2 + ry**2)
    ax_sun = - G * sun_mass * rx / (r_sun**3)
    ay_sun = - G * sun_mass * ry / (r_sun**3)
    # Acceleration due to Earth (treated as a point mass)
    dx = ex - rx
    dy = ey - ry
    r_earth = math.sqrt(dx**2 + dy**2)
    ax_earth = G * earth_mass * dx / (r_earth**3)
    ay_earth = G * earth_mass * dy / (r_earth**3)
    return ax_sun + ax_earth, ay_sun + ay_earth

class Rocket:
    def __init__(self, x, y, vx, vy):
        #METERS_PER_PIXEL = 1e-6
        self.sim_x = x
        self.sim_y = y
        self.vx = vx
        self.vy = vy
        self.trail = []
        self.trail_length = 100
        self.trail_color = (100, 100, 255)
        self.launched = False  

    def update(self, dt, earth_x, earth_y, G, sun_mass, earth_mass):
        if self.launched:
            # Use velocity Verlet integration
            ax_old, ay_old = rocket_acceleration(self.sim_x, self.sim_y, earth_x, earth_y, G, sun_mass, earth_mass)
            new_x = self.sim_x + self.vx * dt + 0.5 * ax_old * dt**2
            new_y = self.sim_y + self.vy * dt + 0.5 * ay_old * dt**2
            ax_new, ay_new = rocket_acceleration(new_x, new_y, earth_x, earth_y, G, sun_mass, earth_mass)
            self.vx = self.vx + 0.5 * (ax_old + ax_new) * dt
            self.vy = self.vy + 0.5 * (ay_old + ay_new) * dt
            self.sim_x = new_x
            self.sim_y = new_y
        else:
            self.sim_x = earth_x
            self.sim_y = earth_y

    def draw(self, screen, current_mpp, sun_x, sun_y):
        pixel_x = int(sun_x + self.sim_x / current_mpp)
        pixel_y = int(sun_y + self.sim_y / current_mpp)
        self.trail.append((pixel_x, pixel_y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
        for point in self.trail:
            pygame.draw.circle(screen, self.trail_color, point, 2)
        pygame.draw.circle(screen, (255, 255, 0), (pixel_x, pixel_y), 10)

# ------------------- Initialization -------------------
pygame.init()
WIDTH, HEIGHT = 1600, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth Orbiting Sun")
YELLOW = (201, 175, 58)
BLACK = (25, 25, 25)
BLUE = (40, 70, 237)
GRID_COLOR = (50, 50, 50)
FPS = 60
clock = pygame.time.Clock()

# Use a fixed time step (TS) in seconds (adjust if necessary for accuracy)
TS = 60 * 60  # 1 hour time step
TIME_SIMULATION = 0

G = 6.67430e-11      # m^3 kg^-1 s^-2
SUN_MASS = 1.989e30   # kg
EARTH_MASS = 5.972e24 # kg
DISTANCE_FROM_SUN_M = 1.4959787e11  # meters
METERS_PER_PIXEL = DISTANCE_FROM_SUN_M / 600

SUN_RADIUS = 50
EARTH_RADIUS = 10

# Sun drawn at center of screen (pixel coordinates)
sun_x = WIDTH // 2
sun_y = HEIGHT // 2

# Earth's initial simulation state (in meters, relative to Sun at (0,0))
earth_x = 147.1e9   # Perihelion distance
earth_y = 0
initial_vy = 30290  # m/s at perihelion
earth_vx = 0
earth_vy = initial_vy

editable_G = G
editable_SUN_MASS = SUN_MASS
editable_EARTH_MASS = EARTH_MASS

zoom_factor = 1.0

# Precompute Earth's initial acceleration using the Sun's gravity.
ax_old, ay_old = earth_acceleration(earth_x, earth_y, editable_G, editable_SUN_MASS)

running = True

# Initialize the rocket at Earth's position with Earth's velocity.
rocket = Rocket(earth_x, earth_y, earth_vx, earth_vy)

# ------------------- Main Loop -------------------
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    current_mpp = METERS_PER_PIXEL / zoom_factor

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Hard reset the simulation.
                earth_x = 147.1e9
                earth_y = 0
                earth_vx = 0
                earth_vy = initial_vy
                editable_G = G
                editable_SUN_MASS = SUN_MASS
                editable_EARTH_MASS = EARTH_MASS
                rocket.trail.clear()
                TIME_SIMULATION = 0
                ax_old, ay_old = earth_acceleration(earth_x, earth_y, editable_G, editable_SUN_MASS)
                rocket.sim_x = earth_x
                rocket.sim_y = earth_y
                rocket.vx = earth_vx
                rocket.vy = earth_vy
                rocket.launched = False
            if event.key == pygame.K_UP:
                TS += 1000
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
                editable_G = G
                editable_SUN_MASS = SUN_MASS
                editable_EARTH_MASS = EARTH_MASS
                zoom_factor = 1.0
                rocket.trail.clear()
                TIME_SIMULATION = 0
                ax_old, ay_old = earth_acceleration(earth_x, earth_y, editable_G, editable_SUN_MASS)
                rocket.sim_x = earth_x
                rocket.sim_y = earth_y
                rocket.vx = earth_vx
                rocket.vy = earth_vy
                rocket.launched = False
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
            if event.key == pygame.K_i:
                zoom_factor *= 1.1
            if event.key == pygame.K_o:
                zoom_factor /= 1.1
            if event.key == pygame.K_l:
                # Launch the rocket if it hasn't been launched.
                if not rocket.launched:
                    rocket.launched = True
                    # Add a boost (adjust the magnitude/direction as needed)
                    rocket.vx += 10000

    draw_dynamic_grid(screen, sun_x, sun_y, WIDTH, HEIGHT, current_mpp, GRID_COLOR)
    # Draw the Sun at its fixed pixel location.
    pygame.draw.circle(screen, YELLOW, (sun_x, sun_y), SUN_RADIUS)

    # ---  Verlet integration ---
    new_earth_x = earth_x + earth_vx * TS + 0.5 * ax_old * TS**2
    new_earth_y = earth_y + earth_vy * TS + 0.5 * ay_old * TS**2
    ax_new, ay_new = earth_acceleration(new_earth_x, new_earth_y, editable_G, editable_SUN_MASS)
    earth_vx = earth_vx + 0.5 * (ax_old + ax_new) * TS
    earth_vy = earth_vy + 0.5 * (ay_old + ay_new) * TS
    earth_x, earth_y = new_earth_x, new_earth_y
    ax_old, ay_old = ax_new, ay_new
    TIME_SIMULATION += TS

    # Earth Energy
    kinetic_energy = 0.5 * editable_EARTH_MASS * (earth_vx**2 + earth_vy**2)
    distance = math.sqrt(earth_x**2 + earth_y**2)
    potential_energy = - editable_G * editable_SUN_MASS * editable_EARTH_MASS / distance
    total_energy = kinetic_energy + potential_energy


    rocket.update(TS, earth_x, earth_y, editable_G, editable_SUN_MASS, editable_EARTH_MASS)
    rocket.draw(screen, current_mpp, sun_x, sun_y)

    # Convert Earth's simulation coordinates to pixel coordinates for drawing.
    earth_x_px = int(sun_x + earth_x / current_mpp)
    earth_y_px = int(sun_y + earth_y / current_mpp)
    pygame.draw.circle(screen, BLUE, (earth_x_px, earth_y_px), EARTH_RADIUS)

    # Display simulation information and energy values.
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(f"Earth Position: ({earth_x:.2e}, {earth_y:.2e}) m", True, (255,255,255))
    screen.blit(text, (10,10))
    text = font.render(f"Earth Velocity: ({earth_vx:.2e}, {earth_vy:.2e}) m/s", True, (255,255,255))
    screen.blit(text, (10,40))
    text = font.render(f"Distance from Sun: {distance:.2e} m", True, (255,255,255))
    screen.blit(text, (10,70))
    text = font.render(f"Gravitational Force: {editable_G * editable_SUN_MASS * editable_EARTH_MASS / distance**2:.2e} N", True, (255,255,255))
    screen.blit(text, (10,100))
    text = font.render(f"Acceleration: ({ax_new:.2e}, {ay_new:.2e}) m/s²", True, (255,255,255))
    screen.blit(text, (10,130))
    decade = int(TIME_SIMULATION // (60 * 60 * 24 * 10))
    year = int(TIME_SIMULATION // (60 * 60 * 24 * 365))
    days = int(TIME_SIMULATION // (60 * 60 * 24))
    hours = int((TIME_SIMULATION % (60 * 60 * 24)) // (60 * 60))
    time_display = f"Sim Time: {year}y {days}d {hours}hs"
    text_surface = font.render(time_display, True, (255,255,255))
    screen.blit(text_surface, (10,160))
    edit1 = font.render(f"[←][→] Earth Initial VY: {initial_vy} m/s", True, (180,180,255))
    edit2 = font.render(f"[↑][↓] Time Step (TS): {TS} s", True, (180,180,255))
    edit3 = font.render(f"[R] Reset Simulation   [SPACE] Hard Reset", True, (180,180,255))
    edit4 = font.render(f"[Z+][X-] Sun Gravity: {editable_G:.2e}", True, (180,180,255))
    edit5 = font.render(f"[C+][V-] Sun Mass: {editable_SUN_MASS:.2e} kg", True, (180,180,255))
    edit6 = font.render(f"[B+][N-] Earth Mass: {editable_EARTH_MASS:.2e} kg", True, (180,180,255))
    edit7 = font.render(f"[I] Zoom In  [O] Zoom Out  Zoom Factor: {zoom_factor:.2f}", True, (180,180,255))
    edit8 = font.render(f"[L] Launch Rocket", True, (180,180,255))
    screen.blit(edit8, (10,150))
    screen.blit(edit1, (10,190))
    screen.blit(edit2, (10,220))
    screen.blit(edit3, (10,250))
    screen.blit(edit4, (10,280))
    screen.blit(edit5, (10,310))
    screen.blit(edit6, (10,340))
    screen.blit(edit7, (10,370))
    energy1 = font.render(f"Kinetic Energy: {kinetic_energy:.2e} J", True, (180,180,255))
    energy2 = font.render(f"Potential Energy: {potential_energy:.2e} J", True, (180,180,255))
    energy3 = font.render(f"Total Energy: {total_energy:.2e} J", True, (180,180,255))
    screen.blit(energy1, (10,400))
    screen.blit(energy2, (10,430))
    screen.blit(energy3, (10,460))

    pygame.display.flip()

pygame.quit()
