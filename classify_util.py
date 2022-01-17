
import os
import shutil
import pygame as pg

pg.init()


class C:
    BLACK = (0, 0, 0)
    BG = (43, 43, 43)



width, height = 1280, 960

screen = pg.display.set_mode((width, height), pg.RESIZABLE)
screen.fill(C.BG)
pg.display.flip()


# print(pg.font.get_fonts())
font = pg.font.SysFont('nanumgothic', 20, False, False)
def text(t, c=None):
    if c is None:
        c = C.BLACK
    return font.render(t, True, c)


clock = pg.time.Clock()
fps = 75

render_updated = False
def updated():
    global render_updated
    render_updated = True
running = True
cnt = 0
while running:
    cnt += 1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.VIDEORESIZE:
            width, height = screen.get_size()
            print(width, height)
            updated()



    if render_updated:
        screen.fill(C.BG)

        pg.display.flip()

        render_updated = False

    clock.tick(fps)



