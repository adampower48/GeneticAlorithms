# Following tutorial at
# http://www.pymunk.org/en/latest/tutorials/SlideAndPinJoint.html

import random
import sys

import pygame
import pymunk
import pymunk.pygame_util
from pygame.locals import *


def main():
    # Window setup
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    # Environment parameters
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

    lines = add_L(space)  # Create lines
    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)  # This handles drawing all the objects

    ticks_to_next_ball = 10
    while True:
        # Handles keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        # Spawns balls with delay in between
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        # Delete balls that are off screen
        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 0:  # 1
                balls_to_remove.append(ball)  # 2

        for ball in balls_to_remove:
            space.remove(ball, ball.body)  # 3
            balls.remove(ball)  # 4

        # Advance time by 0.02s
        space.step(1 / 50.0)

        # Display stuff
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)  # Also for drawing all objects

        pygame.display.flip()
        clock.tick(50)


def add_L(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # 1
    rotation_limit_body.position = (200, 300)

    body = pymunk.Body(10, 10000)
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100, 0), (0, 0), 0, joint_limit)  # 2

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return l1, l2


def add_static_L(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)  # 1
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (255, 0), 5)  # 2
    l2 = pymunk.Segment(body, (-150, 0), (-150, 50), 5)

    space.add(l1, l2)  # 3
    return l1, l2


def draw_lines(screen, lines):
    # Not used in main code, just to show how it would be done
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)  # 1
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)  # 2
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, (200, 200, 200), False, [p1, p2])


def add_ball(space):
    mass = 1
    radius = 14
    moment = pymunk.moment_for_circle(mass, 0, radius)  # 1
    body = pymunk.Body(mass, moment)  # 2
    x = random.randint(120, 380)
    body.position = x, 550  # 3
    shape = pymunk.Circle(body, radius)  # 4
    space.add(body, shape)  # 5
    return shape


def draw_ball(screen, ball):
    # Not used, just to show how it would work
    p = int(ball.body.position.x), 600 - int(ball.body.position.y)
    pygame.draw.circle(screen, (0, 0, 255), p, int(ball.radius), 2)


def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y + 600)


if __name__ == '__main__':
    sys.exit(main())
