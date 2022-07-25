import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()
        self.color = color
        self.backcolor = None
        self.pos = (x, y) 
        self.width = w
        self.height = h

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([self.width, self.height])
       self.image.fill(self.color)

       self.rect = self.image.get_rect()
       self.rect.move_ip(self.pos)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    # `event.pos` is the mouse position.
                    if self.rect.collidepoint(event.pos):
                        # logic here - 
                        print("pressed")
    

