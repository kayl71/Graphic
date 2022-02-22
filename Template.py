import pygame as pg
import numpy as np
import taichi as ti
import taichi_glsl as ts
import math
import taichi_glsl
from taichi_glsl import vec2, vec3

ti.init(arch=ti.cuda)
FPS = 60
resolution = width, height = (1200, 700)
world_size = (1000, 1000)

@ti.data_oriented
class PyShader:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0,0,0], np.uint8)
        self.screen_field = ti.Vector.field(3, ti.uint8, (width, height))
        self.world = ti.field(dtype = ti.uint8, shape = world_size)
        self.world_temp = ti.field(dtype = ti.uint8, shape = world_size)

    @ti.kernel
    def worldUpdate(self):
        pass

    @ti.kernel
    def create_pict(self):
        # Shader Core (Basic logic)
        k = width/height
            
        for frag_coord in ti.grouped(self.screen_field):
            col = vec3(0)
            self.screen_field[frag_coord.x, frag_coord.y] = col * 255

    @ti.kernel
    def worldStart(self):
        pass

    def start(self):
        self.worldStart()

    def update(self):
        #time = pg.time.get_ticks() * 1e-3
        self.worldUpdate()
        
    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def render(self):
        self.create_pict()
        self.screen_array = self.screen_field.to_numpy()
        self.draw()

    def click(self):
        pass


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(resolution)
        self.clock = pg.time.Clock()
        self.shader = PyShader(self)
        

    def run(self):
        running = True
        self.shader.start()
        updater = False
        world_speed = 1 #moves in sec

        WPS = 1000/world_speed
        last_time_world_update = pg.time.get_ticks()
        while running:
            mouse_pos = pg.mouse.get_pos()

            if updater and pg.time.get_ticks() - last_time_world_update >= WPS:
                self.shader.update()
                last_time_world_update = pg.time.get_ticks()
                
            self.shader.render()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.clock.tick(FPS)
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')



if __name__ == '__main__':
    app = App()
    app.run()
