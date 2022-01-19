
import os
import shutil
import pygame as pg
from typing import Union, List
import random as rd

pg.init()

class C:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BG = (32, 32, 32)
pre_f_sizes = [10, 12, 16, 20, 32]
font_size = {
    i: pg.font.SysFont('nanumgothic', i, False, False) for i in pre_f_sizes
}
def font(size):
    if size not in font_size:
        font_size[size] = pg.font.SysFont('nanumgothic', size, False, False)
    return font_size[size]


def text(t, size=20, c=None):
    if c is None:
        c = C.WHITE
    return font(size).render(t, True, c)
def textp(t, size=20, c=None):
    lines = t.split('\n')
    _w, _h = 0, 0
    _surfs = []
    for _l in lines:
        _tsurf = text(_l, size, c)
        _surfs.append((_tsurf, _h))
        _ww, _hh = _tsurf.get_size()
        if _ww > _w:
            _w = _ww
        _h += _hh
    _surf = pg.Surface((_w, _h), pg.SRCALPHA, 32)
    for _tsurf, _hh in _surfs:
        _surf.blit(_tsurf, (0, _hh))
    return _surf


target_path = 'no_git/imgs'
class_path = 'no_git/classes'
classes = [path for path in os.listdir(class_path) if os.path.isdir(os.path.join(class_path, path))]

n_classes = len(classes)
class_key = [
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'
]
class_pg = [
    pg.K_q, pg.K_w, pg.K_e, pg.K_r, pg.K_t, pg.K_y, pg.K_u, pg.K_i, pg.K_o, pg.K_p
]

classes_str = '\n'.join(map(
    lambda c: '{}: {}'.format(class_key[c[0]], c[1]),
    enumerate(classes)
))
print(classes_str)
c_str_surf = textp(classes_str, 20)

width, height = 1280, 960


def load_image(path):
    _img = pg.image.load(path)
    _w, _h = _img.get_size()
    return _img, (_w, _h)

def resize_fill(img_surf):
    _w, _h = img_surf.get_size()
    _ratio = min(width / _w, height / _h)
    _rw, _rh = int(_w * _ratio), int(_h * _ratio)
    return pg.transform.scale(img_surf, (_rw, _rh))
image_files = os.listdir(target_path)
rd.shuffle(image_files)
print(image_files)
cur_img_file = image_files[0]
cur_img_surf, (cur_w, cur_h) = load_image(os.path.join(target_path, cur_img_file))
cur_img_meta = textp(
    '\n'.join((cur_img_file, '{}x{}'.format(cur_w, cur_h))), 16
)



screen = pg.display.set_mode((width, height), pg.RESIZABLE)

def blit_screen_center(surf):
    _w, _h = surf.get_size()
    _pos = ((width - _w) // 2, (height - _h) // 2)
    screen.blit(surf, _pos)
def draw():
    print('draw')
    screen.fill(C.BG)

    if cur_img_surf is not None:
        img_surf_resized = resize_fill(cur_img_surf)
        blit_screen_center(img_surf_resized)
        screen.blit(cur_img_meta, (0, 0))

    screen.blit(c_str_surf, (0, height - c_str_surf.get_height()))

    pg.display.flip()

draw()




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
        draw()

        render_updated = False

    clock.tick(fps)



