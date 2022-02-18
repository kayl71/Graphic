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
camera_speed = 1
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
        size = 1
        for x, y in self.world_temp:
            count = 0
            for i in range(-size, size+1):
                for j in range(-size, size+1):
                    count += self.world[x+i, y+j]
                    
            if self.world[x, y] > 0:
                count-=1
                if count == 2 or count == 3:
                    self.world_temp[x, y] = 1
                else:
                    self.world_temp[x, y] = 0
            elif count == 3:
                self.world_temp[x, y] = 1
            else:
                self.world_temp[x, y] = 0

        for x, y in self.world:
            self.world[x, y] = self.world_temp[x, y]

    @ti.kernel
    def create_pict(self, camera_pos_x : ti.int32, camera_pos_y : ti.int32, squard_size : float):
        # Shader Core (Basic logic)
        k = width/height
            
        for frag_coord in ti.grouped(self.screen_field):
            col = vec3(self.world[camera_pos_x + frag_coord.x//squard_size,
                                 camera_pos_y + frag_coord.y // squard_size] % 255)
            self.screen_field[frag_coord.x, frag_coord.y] = col * 255

    @ti.kernel
    def worldStart(self):
        for x, y in self.world:
            self.world[x, y] = ti.cast(ti.random(int)%2, ti.uint8)
            self.world_temp[x, y] = self.world[x, y]

    def start(self):
        self.worldStart()

    def update(self):
        #time = pg.time.get_ticks() * 1e-3
        self.worldUpdate()
        
    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def render(self, camera_pos, squard_size):
        self.create_pict(camera_pos[0], camera_pos[1], squard_size)
        self.screen_array = self.screen_field.to_numpy()
        self.draw()

    def click(self, mouse_pos, camera_pos, squard_size):
        x = int(camera_pos[0] + mouse_pos[0]/squard_size)
        y = int(camera_pos[1] + mouse_pos[1]/squard_size)
        self.world[x, y] = 1 - self.world[x, y]


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(resolution)
        self.clock = pg.time.Clock()
        self.shader = PyShader(self)
        

    def run(self):
        running = True
        self.shader.start()
        camera_pos = [0, 0]
        updater = False
        move_x = 0
        move_y = 0
        squard_size = 1.0
        world_speed = 1 #moves in sec

        WPS = 1000/world_speed
        last_time_world_update = pg.time.get_ticks()
        while running:
            mouse_pos = pg.mouse.get_pos()

            if updater and pg.time.get_ticks() - last_time_world_update >= WPS:
                self.shader.update()
                last_time_world_update = pg.time.get_ticks()
                
            self.shader.render(camera_pos, squard_size)
            pg.display.flip()
            camera_pos[0] += move_x*camera_speed
            camera_pos[1] += move_y*camera_speed
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    key = event.key
                    if key == pg.K_UP:
                        move_y = -1
                    elif key == pg.K_RIGHT:
                        move_x = 1
                    elif key == pg.K_DOWN:
                        move_y = 1
                    elif key == pg.K_LEFT:
                        move_x = -1
                    elif key == pg.K_SPACE:
                        updater = not updater
                    elif key == pg.K_EQUALS:
                        squard_size += 1
                    elif key == pg.K_MINUS and squard_size > 1:
                        squard_size -= 1
                    elif key == pg.K_q and world_speed > 1:
                        world_speed -= 1
                        WPS = 1000/world_speed
                    elif key == pg.K_e:
                        world_speed += 1
                        WPS = 1000/world_speed

                if event.type == pg.KEYUP:
                    if key == pg.K_UP or key == pg.K_DOWN:
                        move_y = 0
                    elif key == pg.K_RIGHT or key == pg.K_LEFT:
                        move_x = 0

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.shader.click(mouse_pos, camera_pos, squard_size)

                elif event.type == pg.QUIT:
                    running = False

            self.clock.tick(FPS)
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')



if __name__ == '__main__':
    app = App()
    app.run()
