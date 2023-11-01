font = pygame.font.Font(None, 25)
text = font.render("You win!", True, BLACK)
text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
screen.blit(text, text_rect)
