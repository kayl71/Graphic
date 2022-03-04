import pygame as pg
import math


FPS = 60
resolution = width, height = (1200, 700)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pg.display.set_mode(resolution)
clock = pg.time.Clock()

running = True

balls = [ 
    [(2, 2), [5, 5], 100],
    [(200, 200), [-5, 5], 100],
    [(10, 400), [5, -5], 100]
    ]

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
    for i in range(len(balls)):
        centres[i] = (balls[i][0][0] + balls[i][2]/2, balls[i][0][1] + balls[i][2]/2)

    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            r = ((centres[i][1] - centres[j][1])**2 + (centres[i][0] - centres[j][0])**2)**(1/2)
            if r <= (balls[i][2] + balls[j][2])/2:
                balls[i][1][0] *= -1
                balls[i][1][1] *= -1
                balls[j][1][0] *= -1
                balls[j][1][1] *= -1



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
