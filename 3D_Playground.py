"""
Joseph Nuttall
Comp Sci 2
Final Project: 3D Playground
Let user modify and mess with 3d shaped using both mouse and keyboard controls
"""

import pygame
import copy
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


#START GRAPHICS#
pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
###INITIALIZE
# fonts
DESCRIPTOR = pygame.font.SysFont('Impact', 40)
FONT = pygame.font.SysFont('Impact', 90)
# end fonts
clock = pygame.time.Clock()
###END INITIALIZE

def draw_shape(edges, vertices):
    glBegin(GL_LINES) #Start drawing/making shaped
    for edge in edges:
        for vertex in edge:
            glVertex(vertices[vertex]) #Sets the vertexes from edges list
    glEnd() #Done making shapes

def move_shape(vertice_list, mouse_x, mouse_y, back_vertice_list):


    center = [(mouse_x-960)/220, (540-mouse_y)/160, 0]
    print(center)
    for i in range(len(vertice_list)):
        for j in range(len(vertice_list[i])):

            vertice_list[i][j] = center[j] + back_vertice_list[i][j]
"""
GAME BUTTON CLASS
"""


class GameButton:
    def __init__(self, butt_x, butt_y, width, height, description):
        self.hover = False
        self.height = height
        self.width = width
        self.butt_x = butt_x
        self.butt_y = butt_y
        self.description = description

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.butt_x + (width / 2), self.butt_y + (height / 2))

    def draw(self):

        if self.hover == True:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)
            text_surface = DESCRIPTOR.render(self.description, False, (0, 0, 0))
            rect_text = text_surface.get_rect(center=(WIDTH / 2, 900))
            screen.blit(text_surface, (rect_text))

        if self.hover == False:
            pygame.draw.rect(screen, (0, 0, 0), self.rect)
"""
HERE ARE ALL OF THE SCREENS (MENU, DIAMOND, SQUARE, SPHERE)
"""
###MENU###
def menu():
    """
    Creating a digestable game menu where the user can select the 3d playground of their choice
    """

    # Make Buttons Rect
    diamond_button = GameButton(220, 250, 400, 500, "Play With a Diamond")
    cube_button = GameButton(760, 250, 400, 500, "Play With a Cube")
    sphere_button = GameButton(1300, 250, 400, 500, "Play With a Sphere")

    mode_rects = [diamond_button, cube_button,
                  sphere_button]  # list of modes to find which one is hovered
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # FIND IF BUTTON PRESSED
            if event.type == pygame.MOUSEBUTTONDOWN:  # if pressed, start game which was pressed
                if diamond_button.rect.collidepoint(event.pos):  # Diamond Selection
                    diamond_playground()

                elif cube_button.rect.collidepoint(event.pos):  # Cube Selection
                    cube_playground()

                elif sphere_button.rect.collidepoint(event.pos):  # Sphere selection
                    sphere_playground()

            # END FIND BUTTON PRESSED

        # HOVER EFFECT
        pos = pygame.mouse.get_pos()  # Get the mouse position
        for mode in mode_rects:
            mode.hover = False  # Reset hover so that hover effect is not permanent
            if mode.rect.collidepoint(
                    pos):  # If the mouse is colliding with the button, turn on hover effect for button
                mode.hover = True
        # END HOVER EFFECT

        screen.fill((48,25,52))  # FILL SCREEN WITH CYAN

        # Make Buttons Display
        for mode in mode_rects:
            mode.draw()
        ###ADD FLAIR TO TITLE###
        pygame.draw.circle(screen, (0, 0, 0), (600, 130), 20)
        pygame.draw.circle(screen, (0, 0, 0), (1320, 130), 20)

        """
        TEXT START
        """
        # DIAMOND BUTTON
        text_surface = FONT.render('DIAMOND', False, (255, 255, 255))
        screen.blit(text_surface, (250, 460))
        # CUBE BUTTON
        text_surface = FONT.render('CUBE', False, (255, 255, 255))
        screen.blit(text_surface, (860, 460))
        # SPHERE BUTTON
        text_surface = FONT.render('SPHERE', False, (255, 255, 255))
        screen.blit(text_surface, (1370, 460))
        # TITLE
        text_surface = FONT.render('3D PLAYGROUND', True, (0, 0, 0))
        screen.blit(text_surface, (640, 80))
        """
        TEXT END
        """
        pygame.display.flip()
        clock.tick(60)
###DIAMOND MODE###
def diamond_playground():
    """
    Displays the full playground game mode for the diamond
    """
    ###3D INITIALIZING###
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL) #Double buffering visuals and enable OpenGl to run in pygame window

    gluPerspective(45, ((WIDTH, HEIGHT)[0]/(WIDTH, HEIGHT)[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    ###SHAPE CHARACTERISTICS###
    # VERTICES OF DIAMOND
    vertices_diamond = [
        [0.5, -0.5, 0.5],
        [0.5, -0.5, -0.5],
        [-0.5, -0.5, -0.5],
        [-0.5, -0.5, 0.5],
        [0, .5, 0],
        [0, -1.5, 0],
    ]
    backup_vertices_diamond = [
        [0.5, -0.5, 0.5],
        [0.5, -0.5, -0.5],
        [-0.5, -0.5, -0.5],
        [-0.5, -0.5, 0.5],
        [0, .5, 0],
        [0, -1.5, 0],
    ]
    # EDGES OF DIAMOND (each number isa  vertex)
    edges_diamond = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Center Square
        (0, 4), (1, 4), (2, 4), (3, 4),  # Connect to Top
        (0, 5), (1, 5), (2, 5), (3, 5)  # Connect to Bottom
    ]
    ###END SHAPE CHARACTERISTICS###


    scale = 1 #No Scaling Base Variable
    rotate = 0 # Slow Rotation Base variable (CHANGE THIS TO NO ROTATION?)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_shape(edges_diamond, vertices_diamond)
                x, y = pygame.mouse.get_pos()
                move_shape(vertices_diamond, x, y, backup_vertices_diamond)

        if pygame.key.get_pressed()[K_1]:
            scale += .001
        if pygame.key.get_pressed()[K_2]:
            scale -= .001
        if pygame.key.get_pressed()[K_RETURN]:
            scale = 1
            rotate = 0
        if pygame.key.get_pressed()[K_3]:
            rotate += .1
        if pygame.key.get_pressed()[K_4]:
            rotate -= .1


        glRotatef(rotate, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glScalef(scale, scale, scale)
        draw_shape(edges_diamond, vertices_diamond)
        pygame.display.flip()
        clock.tick(60)
###CUBE MODE###
def cube_playground():
    """
    Displays the full playground game mode for the cube
    """
    ###3D INITIALIZING###
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL) #Double buffering visuals and enable OpenGl to run in pygame window

    gluPerspective(45, ((WIDTH, HEIGHT)[0]/(WIDTH, HEIGHT)[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    ###SHAPE CHARACTERISTICS###
    # VERTICES OF CUBE
    vertices_cube = [
        [0.5, -0.5, 0.5],
        [0.5, -0.5, -0.5],
        [-0.5, -0.5, -0.5],
        [-0.5, -0.5, 0.5],
        [0.5, 0.5, 0.5],
        [0.5, 0.5, -0.5],
        [-0.5, 0.5, -0.5],
        [-0.5, 0.5, 0.5],

    ]
    backup_vertices_cube= [
        [0.5, -0.5, 0.5],
        [0.5, -0.5, -0.5],
        [-0.5, -0.5, -0.5],
        [-0.5, -0.5, 0.5],
        [0.5, 0.5, 0.5],
        [0.5, 0.5, -0.5],
        [-0.5, 0.5, -0.5],
        [-0.5, 0.5, 0.5],

    ]
    # EDGES OF CUBE (each number isa  vertex)
    edges_cube = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom Square
        (4, 5), (5, 6), (6, 7), (7, 4),  #Top Square
        (0, 4), (1, 5), (2, 6), (3, 7)  #Connect Squares
    ]
    ###END SHAPE CHARACTERISTICS###


    scale = 1 #No Scaling Base Variable
    rotate = 0 # Slow Rotation Base variable (CHANGE THIS TO NO ROTATION?)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_shape(edges_cube, vertices_cube)
                x, y = pygame.mouse.get_pos()
                move_shape(vertices_cube, x, y, backup_vertices_cube)
        if pygame.key.get_pressed()[K_1]:
            scale += .001
        if pygame.key.get_pressed()[K_2]:
            scale -= .001
        if pygame.key.get_pressed()[K_RETURN]:
            scale = 1
            rotate = 0
        if pygame.key.get_pressed()[K_3]:
            rotate += .1
        if pygame.key.get_pressed()[K_4]:
            rotate -= .1


        glRotatef(rotate, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glScalef(scale, scale, scale)
        draw_shape(edges_cube, vertices_cube)
        pygame.display.flip()
        clock.tick(60)

    ###SPHERE MODE###
def sphere_playground():
    """
    Displays the full playground game mode for the cube
    """
    ###3D INITIALIZING###
    pygame.display.set_mode((WIDTH, HEIGHT),DOUBLEBUF | OPENGL)  # Double buffering visuals and enable OpenGl to run in pygame window

    gluPerspective(45, ((WIDTH, HEIGHT)[0] / (WIDTH, HEIGHT)[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    quadrie = gluNewQuadric()
    gluQuadricDrawStyle(quadrie, GLU_FILL)
    gluQuadricNormals(quadrie, GL_SMOOTH)


    scale = 1  # No Scaling Base Variable
    rotate = 0  # Slow Rotation Base variable (CHANGE THIS TO NO ROTATION?)
    numerate = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            ### DIFFICULT MOVEMENT FOR SPHERE###
            if event.type == pygame.MOUSEBUTTONDOWN:
                file_xy_read = open("store_x_y", "r")
                file_xy_write = open("store_x_y", "w")
                numerate += 1
                old_x, old_y = 960, 540
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if numerate >= 2:
                    string1, string2 = file_xy_read.readlines()
                    old_x, old_y = float(string1), float(string2)
                    print(old_x, old_y)
                    ex, why = ((old_x-960)/460), ((old_y-540)/300)

                #FIND DIFFERENCE BETWEEN CURRENT COORDINATES AND PAST COORDINATES TO DECIDE TRANSLATION DISTANCE THAT FITS CURSOR
                glTranslatef(x/460 - old_x/460, -y/300 - -old_y/300, 0)
                #SAVE COORDINATES BEFORE
                file_xy_write.write(str(x))
                file_xy_write.write("\n" + str(y))

        if pygame.key.get_pressed()[K_1]:
            scale += .001
        if pygame.key.get_pressed()[K_2]:
            scale -= .001
        if pygame.key.get_pressed()[K_RETURN]:
            scale = 1
            rotate = 0
        if pygame.key.get_pressed()[K_3]:
            rotate += .1
        if pygame.key.get_pressed()[K_4]:
            rotate -= .1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.2, 0.01, .01)
        #SPHERE
        gluSphere(quadrie, 1, 32, 32)
        glVertex(0, 0,1 * scale)
        glRotatef(rotate, 0, 1, 0)
        glScalef(scale, scale, scale)
        pygame.display.flip()
        clock.tick(60) 
def main():
    menu()






main()
