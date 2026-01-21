import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# ================= INIT =================
pygame.init()
screen = (1000, 700)
pygame.display.set_mode(screen, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Game Balap Motor 3D")

glEnable(GL_DEPTH_TEST)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)

glLightfv(GL_LIGHT0, GL_POSITION, (0, 20, 10, 1))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

gluPerspective(60, screen[0]/screen[1], 0.1, 200)

# ================= MOTOR =================
motor_pos = [0, 0, 0]
motor_angle = 0
speed = 0.15

lap = 1
angle_track = 0

# ================= CAMERA =================
def camera_follow():
    cam_x = motor_pos[0] - math.sin(math.radians(motor_angle)) * 6
    cam_y = 3
    cam_z = motor_pos[2] + math.cos(math.radians(motor_angle)) * 6
    gluLookAt(cam_x, cam_y, cam_z,
              motor_pos[0], 1, motor_pos[2],
              0, 1, 0)

# ================= OBJECT =================
def draw_cube(x, y, z, size, color):
    glColor3fv(color)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(size, size, size)
    glBegin(GL_QUADS)
    vertices = [
        [1,1,-1],[1,-1,-1],[-1,-1,-1],[-1,1,-1],
        [1,1,1],[1,-1,1],[-1,-1,1],[-1,1,1]
    ]
    faces = [
        [0,1,2,3],[4,5,6,7],[0,1,5,4],
        [2,3,7,6],[0,3,7,4],[1,2,6,5]
    ]
    for f in faces:
        for v in f:
            glVertex3fv(vertices[v])
    glEnd()
    glPopMatrix()

# ================= ROAD =================
def draw_road():
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUAD_STRIP)
    for i in range(0, 360, 5):
        rad = math.radians(i)
        x = math.sin(rad) * 20
        z = math.cos(rad) * 20
        glVertex3f(x - 2, 0, z)
        glVertex3f(x + 2, 0, z)
    glEnd()

    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for i in range(0, 360, 10):
        rad = math.radians(i)
        x = math.sin(rad) * 20
        z = math.cos(rad) * 20
        glVertex3f(x, 0.01, z)
        glVertex3f(x, 0.01, z + 1)
    glEnd()

# ================= CROWD =================
def draw_crowd():
    for i in range(0, 360, 15):
        rad = math.radians(i)
        x = math.sin(rad) * 25
        z = math.cos(rad) * 25
        draw_cube(x, 1, z, 0.5, (0.8, 0.3, 0.3))

# ================= PLAYER =================
def draw_player():
    draw_cube(motor_pos[0], 0.5, motor_pos[2], 0.6, (0, 0, 1))
    draw_cube(motor_pos[0], 1.2, motor_pos[2], 0.3, (1, 0.8, 0.6))

# ================= LOOP =================
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        motor_angle += 2
    if keys[K_RIGHT]:
        motor_angle -= 2
    if keys[K_UP]:
        motor_pos[0] += math.sin(math.radians(motor_angle)) * speed
        motor_pos[2] -= math.cos(math.radians(motor_angle)) * speed

    angle_track += speed
    if angle_track >= 360:
        angle_track = 0
        lap += 1
        print("Lap:", lap)

    glClearColor(0.5, 0.7, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    camera_follow()

    draw_road()
    draw_crowd()
    draw_player()

    if lap > 3:
        print("FINISH! RACE COMPLETED")
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
