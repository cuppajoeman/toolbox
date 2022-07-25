"""Animated Sieve of Erathosthenes.
"""
import pygame
from random import randint
from typing import List, Tuple
from math import floor

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

# Set the width and height of the screen [width, height]
HEIGHT = 800
WIDTH = 800
SCREEN_SIZE = (WIDTH, HEIGHT)
SQRT_N = 16
N = SQRT_N * SQRT_N

SQUARE_SIZE = WIDTH // SQRT_N


def initialize_pygame() -> pygame.Surface:
    """Initialize pygame and the display window."""
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Sieve of Eratosthenes")
    return screen


def draw_grid(screen: pygame.Surface) -> None:
    """Draw the initial grid of numbers."""
    MY_FONT = pygame.font.SysFont('inconsolata', floor(SQUARE_SIZE/2))
    for i in range(SQRT_N):
        for j in range(SQRT_N):
            rect = pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE,
                               SQUARE_SIZE, SQUARE_SIZE)

            # Draw the rectangle
            pygame.draw.rect(screen, BLACK, rect, 2)

            # Draw the text
            k = i + j * SQRT_N
            textsurface = MY_FONT.render(str(k), False, (0, 0, 0))
            text_size = MY_FONT.size(str(k))[0]
            screen.blit(textsurface,
                        (int(SQUARE_SIZE * (i + 0.5) - text_size / 2),
                         int(SQUARE_SIZE * (j + 0.5) - text_size / 2)))


def animated_sieve_of_eratosthenes(screen: pygame.Surface) -> List[bool]:
    """Return a list recording the prime numbers between 1 and N inclusive.

    The returned list has length N, where the boolean at position i represents
    whether the number i is prime.

    Also, animates the sieve onto the given screen.

    Precondition: N >= 2.
    """
    primes = [True] * N

    # 0 and 1 are not prime by definition.
    primes[0] = False
    draw_square(screen, 0, GRAY)
    primes[1] = False
    draw_square(screen, 1, GRAY)

    for i in range(2, SQRT_N):
        shade = (randint(0, 255), randint(0, 255), randint(0, 255))
        if primes[i]:
            # We can start at i * i since we have already accounted for the
            # multiples less than i.
            for j in range(i * i, N, i):
                primes[j] = False
                draw_square(screen, j, shade)
                pygame.display.flip()
                clock.tick(10)
    return primes


def draw_square(screen: pygame.Surface, k: int,
                shade: Tuple[int, int, int]) -> None:
    """Draw a square on the screen for the given number with the given colour.
    """
    j, i = divmod(k, SQRT_N)
    rect = pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, shade, rect)


def save_image(display: pygame.Surface, name: str, pos: Tuple[int, int], size: Tuple[int, int]) -> None:
    image = pygame.Surface(size)  # Create image surface
    image.blit(display, (0, 0), (pos, size))  # Blit portion of the display to the image
    pygame.image.save(image, name)  # Save the image to the disk


if __name__ == '__main__':
    screen = initialize_pygame()

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    done = False

    # --- Screen-clearing code goes here
    screen.fill(WHITE)
    draw_grid(screen)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    animated_sieve_of_eratosthenes(screen)

    # Save the image
    # save_image(screen, 'tmp.jpg', (0, 0), SCREEN_SIZE)

    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    # Close the window and quit.
    pygame.quit()

