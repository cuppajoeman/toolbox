import pygame
import random
import math
import time

# Pygame Initialization
pygame.init()

# Screen Parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Helper Function to Generate Random Flock Parameters
def generate_random_flock_params():
    return {
        "align_radius": random.uniform(30, 70),
        "cohesion_radius": random.uniform(40, 80),
        "separation_radius": random.uniform(20, 50),
        "max_speed": random.uniform(3, 5),
        "max_force": random.uniform(0.03, 0.07),
        "align_strength": random.uniform(0.8, 1.5),
        "cohesion_strength": random.uniform(0.9, 1.2),
        "separation_strength": random.uniform(1.2, 1.7)
    }

# Fish Class (Individual Boid)
class Fish:
    def __init__(self, color):
        self.position = pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.velocity.length() > 0:
            self.velocity.normalize_ip()
        self.velocity *= random.uniform(1, 4)
        self.acceleration = pygame.Vector2(0, 0)
        self.color = color

    def update(self):
        # Limit speed
        if self.velocity.length() > 4:
            self.velocity.scale_to_length(4)

        # Update position
        self.position += self.velocity
        self.velocity += self.acceleration

        # Limit the acceleration (to avoid over-accelerating)
        if self.acceleration.length() > 0.05:
            self.acceleration.scale_to_length(0.05)

        # Reset acceleration each cycle
        self.acceleration = pygame.Vector2(0, 0)

        # Wrap around screen
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), 5)

    def flock(self, fish, flock_params, goal_point):
        alignment = self.align(fish, flock_params) * flock_params["align_strength"]
        cohesion = self.cohesion(fish, flock_params) * flock_params["cohesion_strength"]
        separation = self.separation(fish, flock_params) * flock_params["separation_strength"]

        # Move towards the target point within the goal
        goal_force = self.move_towards_goal(goal_point) * 1.2
        self.acceleration += alignment + cohesion + separation + goal_force

    def align(self, fish, flock_params):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in fish:
            if other != self and self.position.distance_to(other.position) < flock_params["align_radius"]:
                steering += other.velocity
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:  # Avoid normalizing zero vector
                steering = steering.normalize() * flock_params["max_speed"] - self.velocity
            if steering.length() > flock_params["max_force"]:
                steering.scale_to_length(flock_params["max_force"])
        return steering

    def cohesion(self, fish, flock_params):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in fish:
            if other != self and self.position.distance_to(other.position) < flock_params["cohesion_radius"]:
                steering += other.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            if steering.length() > 0:  # Avoid normalizing zero vector
                steering = steering.normalize() * flock_params["max_speed"] - self.velocity
            if steering.length() > flock_params["max_force"]:
                steering.scale_to_length(flock_params["max_force"])
        return steering

    def separation(self, fish, flock_params):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in fish:
            distance = self.position.distance_to(other.position)
            if other != self and distance < flock_params["separation_radius"] and distance > 0:
                diff = self.position - other.position
                diff /= distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:  # Avoid normalizing zero vector
                steering = steering.normalize() * flock_params["max_speed"] - self.velocity
            if steering.length() > flock_params["max_force"]:
                steering.scale_to_length(flock_params["max_force"])
        return steering

    def move_towards_goal(self, goal_point):
        desired = goal_point - self.position
        if desired.length() > 0:
            desired = desired.normalize() * 4
        goal_steering = desired - self.velocity
        if goal_steering.length() > 0.05:
            goal_steering.scale_to_length(0.05)
        return goal_steering

# Flock Class (Collection of Fish)
class Flock:
    def __init__(self, num_fish, color, flock_params, indecisiveness, goal_area):
        self.fish = [Fish(color) for _ in range(num_fish)]
        self.flock_params = flock_params
        self.color = color
        self.indecisiveness = indecisiveness
        self.goal_area = goal_area
        self.goal_point = self.select_goal_point()  # Initial goal point
        self.last_goal_change = time.time()  # Time of the last goal change

    def select_goal_point(self):
        # Randomize goal as a percentage of the goal area
        goal_width, goal_height = self.goal_area.width, self.goal_area.height
        goal_x = self.goal_area.left + random.uniform(0.1, 0.9) * goal_width
        goal_y = self.goal_area.top + random.uniform(0.1, 0.9) * goal_height
        return pygame.Vector2(goal_x, goal_y)

    def update(self):
        current_time = time.time()

        # Randomize goal point within the goal area based on the flock's indecisiveness
        if current_time - self.last_goal_change > self.indecisiveness:
            self.goal_point = self.select_goal_point()
            self.last_goal_change = current_time

        for fish in self.fish:
            fish.flock(self.fish, self.flock_params, self.goal_point)
            fish.update()

    def draw(self, screen):
        for fish in self.fish:
            fish.draw(screen)

# Main Loop
def main():
    goal_area = pygame.Rect(600, 250, 200, 200)
    is_dragging_goal = False

    # Generate a random number of flocks between 2 and 5
    num_flocks = random.randint(2, 5)
    flocks = []

    for _ in range(num_flocks):
        flock_params = generate_random_flock_params()
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        indecisiveness = random.uniform(10, 20)
        flock = Flock(30, color, flock_params, indecisiveness, goal_area)
        flocks.append(flock)

    running = True

    while running:
        screen.fill(WHITE)

        # Draw the goal area
        pygame.draw.rect(screen, BLACK, goal_area, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and goal_area.collidepoint(event.pos):
                    is_dragging_goal = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging_goal = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    goal_area.inflate_ip(0, 10)
                elif event.key == pygame.K_DOWN:
                    goal_area.inflate_ip(0, -10)
                elif event.key == pygame.K_LEFT:
                    goal_area.inflate_ip(-10, 0)
                elif event.key == pygame.K_RIGHT:
                    goal_area.inflate_ip(10, 0)

        if is_dragging_goal:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            goal_area.topleft = (mouse_x - goal_area.width // 2, mouse_y - goal_area.height // 2)

        for flock in flocks:
            flock.update()
            flock.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
