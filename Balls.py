import pygame as pg
import math
import random


FPS = 60
resolution = width, height = (1200, 700)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pg.display.set_mode(resolution)
clock = pg.time.Clock()

running = True

ballCount = 20

balls = [0]*ballCount

for i in range(ballCount):
    balls[i] = [0]*3
    balls[i][0] = (random.randint(0, width-80), random.randint(0, height-80))
    balls[i][1] = [random.randint(5, 12), random.randint(5, 12)]
    balls[i][2] = random.randint(40, 80)


def BallsUpdate():
    global balls
    for i in range(len(balls)):
        ballCoord = balls[i][0]
        ballSpeed = balls[i][1]
        ballSize = balls[i][2]
        if ballCoord[0] + ballSize >= resolution[0] or ballCoord[0] <= 0:
            ballSpeed[0]*=-1
        if ballCoord[1] + ballSize >= resolution[1] or ballCoord[1] <= 0:
            ballSpeed[1]*=-1
        
        balls[i][0] = (ballCoord[0] + ballSpeed[0], ballCoord[1] + ballSpeed[1])
        balls[i][1] = ballSpeed

def BallsRender():
    global screen, balls
    for i in range(len(balls)):
        screen.blit(ballSurfs[i], balls[i][0])

def BallsCollision():
    global balls
    centres = [0]*len(balls)
    speeds = [0]*len(balls)
    for i in range(len(balls)):
        centres[i] = (balls[i][0][0] + balls[i][2]/2, balls[i][0][1] + balls[i][2]/2)
        speeds[i] = (balls[i][1][0]**2 + balls[i][1][1]**2)**(1/2)

    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            y = centres[i][1] - centres[j][1]
            x = centres[i][0] - centres[j][0]
            r = (x**2 + y**2)**(1/2)
            if r <= (balls[i][2] + balls[j][2])/2:
                balls[i][1][0] = speeds[i]*x/r
                balls[i][1][1] = speeds[i]*y/r
                balls[j][1][0] = -speeds[j]*x/r
                balls[j][1][1] = -speeds[j]*y/r



ballSurfs = [0]*len(balls)
for i in range(len(balls)):
    ballSurfs[i] = pg.Surface((balls[i][2], balls[i][2]))
    pg.draw.circle(ballSurfs[i], WHITE, (balls[i][2]/2, balls[i][2]/2), balls[i][2]/2)


while running:
    screen.fill(BLACK)

    BallsUpdate()
    BallsRender()
    BallsCollision()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'FPS: {clock.get_fps() :.2f}')

pg.quit()

