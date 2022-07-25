from typing import List, Set, Tuple
from pygame.colordict import THECOLORS

import pygame
import math
import pygame

clock = pygame.time.Clock()


def convex_hull(points: Set[Tuple[int, int]], screen: pygame.Surface, animate_algorithm: bool) -> List[Tuple[int, int]]:
    """Return the convex hull of the given points.

    The first point in the convex hull is the one with the smallest x-coordinate,
    breaking ties by picking the point with the smallest y-coordinate.
    The points in the convex hull appear in clockwise order.

    Preconditions:
        - len(points) >= 3

    >>> pts = {(200, 100), (250, 200), (500, 300), (425, 100), (150, 350), (700, 30), (500, 500)}
    >>> convex_hull(pts)
    [(150, 350), (200, 100), (700, 30), (500, 500), (150, 350)]
    >>> points2 = {(125, 400), (375, 125), (675, 450)}
    >>> convex_hull(points2)
    [(125, 400), (375, 125), (675, 450), (125, 400)]
    """

    if animate_algorithm:
        for p in points:
            pygame.draw.circle(screen, THECOLORS['white'], p, 3)

    pygame.display.flip()


    starting_point = leftmost(points)
    special_point = (starting_point[0], starting_point[1] + 1)
    second_point = next_point(special_point, starting_point, points, screen, animate_algorithm)


    convex_hull_so_far = [starting_point, second_point]
    while len(convex_hull_so_far) == 1 or starting_point != convex_hull_so_far[-1]:
        prev = convex_hull_so_far[-2]
        np = next_point(prev, convex_hull_so_far[-1], points, screen, animate_algorithm)

        convex_hull_so_far.append(np)

    # After the while loop is done then we have a full convex hull
    for i in range(0, len(convex_hull_so_far)):
        pygame.draw.circle(screen, THECOLORS['gold'], convex_hull_so_far[i], 6)

        if i + 1 < len(convex_hull_so_far):
            pygame.draw.line(screen, THECOLORS['gold'], convex_hull_so_far[i], convex_hull_so_far[i+1], 6)

        #if i > 0:
        #    pygame.draw.line(screen, THECOLORS['darkturquoise'], convex_hull_so_far[i - 1], convex_hull_so_far[i])

    pygame.draw.line(screen, THECOLORS['gold'], convex_hull_so_far[len(convex_hull_so_far) - 1], convex_hull_so_far[0], 6)
        
    pygame.display.flip()
    pygame.time.wait(1000)

    return convex_hull_so_far


def leftmost(points: Set[Tuple[int, int]]) -> Tuple[int, int]:
    """Return the leftmost (smallest x-coordinate) point in points.

    If there is a tie, return the one with the smallest y-coordinate.

    Note: because we're using pygame's coordinate system here, small y-coordinates
    translate to *higher* points in the visualization window.

    Preconditions:
        - points != set()

    >>> pts = {(200, 100), (250, 200), (500, 300), (425, 100), (150, 350), (700, 30), (500, 500)}
    >>> leftmost(pts)
    (150, 350)
    """
    # Version 1, using a loop
    leftmost_so_far = (math.inf, math.inf)

    for p in points:
        if p[0] < leftmost_so_far[0]:
            leftmost_so_far = p
        elif p[0] == leftmost_so_far[0] and p[1] < leftmost_so_far[1]:
            leftmost_so_far = p

    return leftmost_so_far

    # Version 2, using the min function (since tuples are compared lexicographically)
    # return min(points)


def angle_between(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]) -> float:
    """Return the angle between line segments ab and ac, in radians. The formula is derived from
    the geometric definition of the dot product.

    For any vectors, a, b, and theta being the angle between them
    
    a * b =D= ||a||  ||b|| cos(theta)

    Preconditions:
        - b != a
        - c != a

    Hint: The `math` module has a function that you need!

    >>> result = angle_between((150, 350), (150, 351), (200, 100))
    >>> math.isclose(result, 2.9441970937399122)
    True

    Note: to avoid rounding error, you should use min and max to make sure
    your "cos" values are between -1 and 1.
    """
    numerator = (b[0] - a[0]) * (c[0] - a[0]) + (b[1] - a[1]) * (c[1] - a[1])
    denominator = math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) \
        * math.sqrt((c[0] - a[0]) ** 2 + (c[1] - a[1]) ** 2)

    return math.acos(max(-1.0, min(1.0, numerator / denominator)))


def next_point(prev: Tuple[int, int], curr: Tuple[int, int], points: Set[Tuple[int, int]], screen: pygame.Surface, animate_algorithm: bool) -> Tuple[int, int]:
    """Return the next point in the convex hull after curr and prev.

    If there is a tie in the angle calculation, pick the point that is *furthest* away from curr.

    Preconditions:
      - len(points) >= 3
      - curr in points
      - curr and prev are both in the convex hull of points

    Implementation notes:
        - Call angle_between, but make sure you are passing in the arguments in the correct order
        - curr is in points; you need to skip over this point to ensure you don't violate a
          precondition for angle_between

    >>> pts = {(200, 100), (250, 200), (500, 300), (425, 100), (150, 350), (700, 30), (500, 500)}
    >>> next_point((150, 351), (150, 350), pts)
    (200, 100)
    """
    # Version 1, using a loop
    max_angle = 0
    max_angle_point = None

    for q in points:
        if q != curr:
            theta = angle_between(curr, prev, q)

            if animate_algorithm:
                pygame.draw.line(screen, THECOLORS['blue'], curr, q)
                pygame.time.wait(10)
            pygame.display.flip()

            if max_angle_point is None:
                max_angle = theta
                max_angle_point = q
            elif theta > max_angle:
                max_angle = theta
                max_angle_point = q
            elif theta == max_angle and math.dist(curr, max_angle_point) < math.dist(curr, q):
                max_angle = theta
                max_angle_point = q

    pygame.draw.line(screen, THECOLORS['red'], curr, max_angle_point, 3)

    return max_angle_point

    # Version 2, using min (and a "key" function)
    # return min(points, key=lambda q: (angle_between(curr, prev, q), - math.dist(curr, q)))



def draw_hull(screen: pygame.Surface, points: List[Tuple[int, int]]) -> None:
    """Render points as turquoise circles and adjacent points as turquoise lines onto the screen.

    Preconditions:
        - all(0 <= p[0] < screen.width for p in points)  # x-coordinates in range
        - all(0 <= p[1] < screen.height for p in points)  # y-coordinates in range
    """


def animate_convex_hull(points: Set[Tuple[int, int]]) -> None:
    """Animate the convex hull algorithm using pygame."""

    pygame.init()
    screen_size = (800, 800)


    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Convex Hull Generator')
    screen.fill(THECOLORS['black'])

    hull = convex_hull(points, screen, True)
    #assert len(hull) >= 3

    #hull_so_far = [hull[0], hull[1]]
    #current_index = 2

    # Start the event loop
    while True:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the event loop
                pygame.quit()

    #        if event.type == pygame.KEYDOWN:
    #            if event.key == pygame.K_RIGHT and current_index < len(hull):
    #                list.append(hull_so_far, hull[current_index])
    #                current_index = current_index + 1
    #            elif event.key == pygame.K_LEFT and current_index > 2:
    #                list.pop(hull_so_far)
    #                current_index = current_index - 1

       # Visualize the hull
       # screen.fill(THECOLORS['white'])
       # draw_points(screen, points)
       # draw_hull(screen, hull_so_far)


if __name__ == '__main__':
    import random

    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800

    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    NUM_POINTS = 25

    font = pygame.font.Font(None, 25)


    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Convex Hull Generator')
    screen.fill(THECOLORS['black'])


    # A random set of points
    RANDOM_POINTS = {(random.randint(10, SCREEN_WIDTH - 10), random.randint(10, SCREEN_HEIGHT - 10))
                     for _ in range(0, NUM_POINTS)}

    #animate_convex_hull(RANDOM_POINTS)
    hull = convex_hull(RANDOM_POINTS, screen, True)

    # Start the event loop
    while True:
        # Process events
        screen.fill(THECOLORS['black'])
        RANDOM_POINTS = {(random.randint(10, SCREEN_WIDTH - 10), random.randint(10, SCREEN_HEIGHT - 10))
                         for _ in range(0, NUM_POINTS)}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the event loop
                pygame.quit()

        hull = convex_hull(RANDOM_POINTS, screen, True)

        screen.fill(THECOLORS['black'])
        text = font.render("Percentage of points part of hull: " + str(len(hull)/NUM_POINTS), True, THECOLORS['white'])
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(1000)

