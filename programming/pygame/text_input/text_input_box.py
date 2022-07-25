import pygame as pg

class TextInputBox(pg.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y) 
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pg.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pg.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pg.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft = self.pos)


    def update(self, event_list):
        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pg.KEYDOWN and self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                    # Put logic on enter here
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()



## initialize pg and create window
pg.init()
#pg.mixer.init()  ## For sound

FPS = 60
WIDTH, HEIGHT = pg.display.Info().current_w, pg.display.Info().current_h

#surface = pg.display.set_mode((WIDTH, HEIGHT))
surface = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN | pg.RESIZABLE )
pg.display.set_caption("Input box")
clock = pg.time.Clock()     ## For syncing the FPS

font = pg.font.SysFont(None, 50)

text_input_box = TextInputBox(WIDTH/2, HEIGHT/2, WIDTH/3, font)

group = pg.sprite.Group(text_input_box)


## Game loop
running = True
while running:

    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    event_list = pg.event.get()
    for event in event_list:        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pg.QUIT:
            running = False

    group.update(event_list)



    #3 Draw/render
    surface.fill(pg.Color('black'))

    
    ########################

    ### Your code comes here

    #draw_menu(surface)
    group.draw(surface)


    ########################

    ## Done after drawing everything to the surface
    pg.display.flip()       

pg.quit()


