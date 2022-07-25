import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,start_pos, width, height,color, movement_keys):
        """
        Initialize a player

        Movement Keys is a set of pygame keys in the following order:
         
        Left Up Right Down (clockwise order)
        """
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.math.Vector2(start_pos)
        self.width = width
        self.height = height
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.movement_vector = pygame.math.Vector2(0,0)
        self.movement_keys = movement_keys

        self.velocity = pygame.math.Vector2(0,0)

        self.max_speed = 4000
        self.acceleration = 2000
        self.friction = 0.05


    def update(self, delta_time):
        keys = pygame.key.get_pressed()

        l, u, r, d = self.movement_keys

        self.movement_vector.x = int(keys[r]) - int(keys[l]) 
        self.movement_vector.y = -(int(keys[u]) - int(keys[d]))

        velocity_change = self.acceleration * delta_time

        if not (self.movement_vector.x == 0 and self.movement_vector.y == 0):
            pygame.math.Vector2.normalize_ip(self.movement_vector)
            self.apply_movement(velocity_change * self.movement_vector)
        else:
            # If no buttons are being pressed then we can apply friction to slow them down
            # We will slow them down at the same speed they would speed up by
            self.apply_friction()

        # Based on our acceleration calculate what the velocity update should be

        # Change in position = velocity * change in time
        self.pos += self.velocity * delta_time
        self.rect.center = self.pos

    
    def apply_friction(self):
        if self.velocity.magnitude() - self.friction > 0:
            self.velocity -= self.velocity * self.friction
        else:
            # If we can't subtract any more, just set it to zero
            self.velocity.x = 0
            self.velocity.y = 0

    def apply_movement(self, new_velocity_update):
        self.velocity += new_velocity_update
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize()  * self.max_speed
        
        
