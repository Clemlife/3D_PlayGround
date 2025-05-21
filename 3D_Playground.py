"""
Joseph Nuttall
Comp Sci 2
Final Project: 3D Playground
Let user modify and mess with 3d shaped using both mouse and keyboard controls
"""

import pygame
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
    """
    Draws shape in space based on edges and vertices
    only used for pyramid and cube
    """

    glBegin(GL_LINES) #Start drawing/making shaped
    for edge in edges:
        for vertex in edge:
            glVertex(vertices[vertex]) #Sets the vertexes from edges list
    glEnd() #Done making shapes

def move_shape(numerate):
    """
    Moves shape to location of mouse press
    """
    #OPEN FILES TO SAVE OLD CLICK LOCATIONS
    file_xy_read = open("store_x_y", "r")
    file_xy_write = open("store_x_y", "a")
    old_x, old_y = 960, 540
    x, y = pygame.mouse.get_pos()

    if numerate > 1: # if past first click, save former x and y values to save file
        string1, string2 = file_xy_read.readlines()
        old_x, old_y = float(string1), float(string2)

    # FIND DIFFERENCE BETWEEN CURRENT COORDINATES AND PAST COORDINATES TO DECIDE TRANSLATION DISTANCE THAT FITS CURSOR
    glTranslatef(x / 460 - old_x / 460, -y / 300 - -old_y / 300, 0)
    # SAVE COORDINATES BEFORE NEXT ROTATION IN ORDER TO ADJUST BASED ON PAST LOCATION
    clear = open("store_x_y", "w")
    file_xy_write.write(str(x))
    file_xy_write.write("\n" + str(y))
    #CLOSE FILES
    file_xy_write.close()
    file_xy_read.close()

"""
GAME BUTTON CLASS
"""
class GameButton:
    """
    CREATES GAME BUTTONS FOR MENU
    """
    def __init__(self, butt_x, butt_y, width, height, description):
        self.hover = False
        self.height = height
        self.width = width
        self.butt_x = butt_x
        self.butt_y = butt_y
        self.description = description

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((0, 0, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (self.butt_x + (width / 2), self.butt_y + (height / 2))

    def draw(self):
        ###HOVER EFFECT
        if self.hover == True:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)
            text_surface = DESCRIPTOR.render(self.description, False, (0, 0, 0))
            rect_text = text_surface.get_rect(center=(WIDTH / 2, 900))
            screen.blit(text_surface, (rect_text))
        ### BASE EFFECT
        if self.hover == False:
            pygame.draw.rect(screen, (200, 0, 0), self.rect)

def draw_sphere(quadrie):
    """
    Creates a sphere that is separated into quadrants for the sphere playground
    """
    ### DRAWING SPHERE ###

    #Enable Clip Planes
    glEnable(GL_CLIP_PLANE0)
    glEnable(GL_CLIP_PLANE1)
    # RED SEMI
    glClipPlane(GL_CLIP_PLANE0, (0, 0, 1, 0))  # Cut sphere in half
    glClipPlane(GL_CLIP_PLANE1, (-1, 0, 0, 0))  # Cut sphere into a quarter
    glColor3f(.9, 0.0, 0.0)
    gluSphere(quadrie, 1, 50, 50)  # Creates sphere, only hemisphere because cut by clip plane
    glDisable(GL_CLIP_PLANE0)  # DISABLE PLANE
    glDisable(GL_CLIP_PLANE1)
    # BLUE SEMI
    glEnable(GL_CLIP_PLANE0)  # ENABLE CLIP PLANE
    glEnable(GL_CLIP_PLANE1)
    glClipPlane(GL_CLIP_PLANE0, (0, 0, -1, 0))  # CLIP IN HALF
    glClipPlane(GL_CLIP_PLANE1, (1, 0, 0, 0))  # CLIP IN HALF AGAIN
    glColor3f(0, 0.0, 1)
    gluSphere(quadrie, 1, 50, 50)  # Create sphere
    glDisable(GL_CLIP_PLANE0)  # DISABLE PLANE
    glDisable(GL_CLIP_PLANE1)
    # GREEN QUART
    glEnable(GL_CLIP_PLANE0)  # ENABLE CLIP PLANE
    glEnable(GL_CLIP_PLANE1)
    glClipPlane(GL_CLIP_PLANE0, (0, 0, -1, 0))  # CLIP IN HALF
    glClipPlane(GL_CLIP_PLANE1, (-1, 0, 0, 1))  # CLIP FIRST HALF IN HALF
    glColor3f(0, 1, 0)
    gluSphere(quadrie, 1, 50, 50)  # Create sphere
    glDisable(GL_CLIP_PLANE0)  # DISABLE PLANE
    glDisable(GL_CLIP_PLANE1)
    # PURP QUART
    glEnable(GL_CLIP_PLANE0)  # ENABLE CLIP PLANE
    glEnable(GL_CLIP_PLANE1)
    glClipPlane(GL_CLIP_PLANE0, (0, 0, 1, 0))  # CLIP IN HALF
    glClipPlane(GL_CLIP_PLANE1, (1, 0, 0, 0))  # CLIP IN HALF AGAIN FOR QUARTER
    glColor3f(.7, .3, 1)
    gluSphere(quadrie, 1, 50, 50)  # Create sphere
    #DISABLE CLIP PLANES
    glDisable(GL_CLIP_PLANE0)
    glDisable(GL_CLIP_PLANE1)
    # END SPHERE
"""
HERE ARE ALL OF THE SCREENS (MENU, DIAMOND, SQUARE, SPHERE)
"""
###MENU###
def menu():
    """
    Creating a digestable game menu where the user can select the 3d playground of their choice
    """
    #REPEAT SCREEN INITIALIZATION, NEEDED TO MOVE FROM 3D GAMEMODES BACK TO MENU
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #END REPEAT INITIALIZATION
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
        pygame.draw.circle(screen, (255, 0, 0), (600, 130), 20)
        pygame.draw.circle(screen, (255, 0, 0), (1320, 130), 20)

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
        text_surface = FONT.render('3D PLAYGROUND', True, (255, 0, 0))
        screen.blit(text_surface, (680, 80))
        """
        TEXT END
        """
        pygame.display.flip()
        clock.tick(60)
###DIAMOND MODE###
def diamond_playground():
    """
    Displays the full playground game mode for the diamond
    The diamond is red and is see through, none of its faces are filled in
    User can press keys to play with diamond:
    1 = grow
    2 = shrink
    Right = Spin right
    Left = Spin left
    Up = Spin up
    Down = Spin down
    Return = stop scaling and rotation
    Click on screen = cube moves to click location (depends on rotation)
    R = return to menu
    """
    ###3D INITIALIZING###
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL) #Double buffering visuals and enable OpenGl to run in pygame window

    gluPerspective(45, ((WIDTH, HEIGHT)[0]/(WIDTH, HEIGHT)[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    ###SHAPE CHARACTERISTICS###
    # VERTICES OF DIAMOND
    vertices_diamond = [
        [0.5, 0, 0.5],
        [0.5, 0, -0.5],
        [-0.5, 0, -0.5],
        [-0.5, 0, 0.5],
        [0, 1, 0],
        [0, -1, 0],
    ]

    # EDGES OF DIAMOND (each number isa  vertex)
    edges_diamond = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Center Square
        (0, 5), (1, 5), (2, 5), (3, 5),  # Connect to Bottom
        (0, 4), (1, 4), (2, 4), (3, 4)  # Connect to Top


    ]
    ###END SHAPE CHARACTERISTICS###

    numerate = 0
    scale = 1 #No Scaling Base Variable
    rotate = 0 # Slow Rotation Base variable (CHANGE THIS TO NO ROTATION?)
    x, y = 0, 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = 0, 0
                numerate += 1
                move_shape(numerate)

        ### KEY INPUTS
        if pygame.key.get_pressed()[K_1]:
            scale += .001
        elif pygame.key.get_pressed()[K_2]:
            scale -= .001
        elif pygame.key.get_pressed()[K_RETURN]:
            scale = 1
            rotate = 0
        elif pygame.key.get_pressed()[K_RIGHT]: #3 to rotate right
            x = 0
            y = 1
            rotate += .4
        elif pygame.key.get_pressed()[K_LEFT]: #4 to rotate left
            x = 0
            y = 1
            rotate -= .4
        elif pygame.key.get_pressed()[K_UP]:
            #2 to shrink
            x = 1
            y=0
            rotate -= .4
        elif pygame.key.get_pressed()[K_DOWN]: #Enter to pause scale and rotation
            x = 1
            y = 0
            rotate += .4
        elif pygame.key.get_pressed()[K_r]:
            menu()
        ### END KEY INPUTS


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(rotate, x, y, 0)
        glScalef(scale, scale, scale)
        glColor(1, 0, 0)
        draw_shape(edges_diamond, vertices_diamond)
        pygame.display.flip()
        clock.tick(60)
###CUBE MODE###
def cube_playground():
    """
    Displays the full playground game mode for the cube:
    The cube will be see through, no faces will be filled in
    User can press keys to play with cube:
    1 = grow
    2 = shrink
    Right = Spin right
    Left = Spin left
    Up = Spin up
    Down = Spin down
    Return = stop scaling and rotation
    Click on screen = cube moves to click location (depends on rotation)
    R = return to menu
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
    # EDGES OF CUBE (each number is a vertex)
    edges_cube = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom Square
        (4, 5), (5, 6), (6, 7), (7, 4),  #Top Square
        (0, 4), (1, 5), (2, 6), (3, 7)  #Connect Squares
    ]
    ###END SHAPE CHARACTERISTICS###

    numerate = 0 #for movement function
    scale = 1 #No Scaling Base Variable
    rotate = 0 # No rotation base variable
    x, y = 0, 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                numerate += 1
                move_shape(numerate)
        ### KEY INPUTS
        if pygame.key.get_pressed()[K_1]:
            scale += .001
        elif pygame.key.get_pressed()[K_2]:
            scale -= .001
        elif pygame.key.get_pressed()[K_RETURN]:
            scale = 1
            rotate = 0
        elif pygame.key.get_pressed()[K_RIGHT]: #3 to rotate right
            x = 0
            y = 1
            rotate += .4
        elif pygame.key.get_pressed()[K_LEFT]: #4 to rotate left
            x = 0
            y = 1
            rotate -= .4
        elif pygame.key.get_pressed()[K_UP]:
            #2 to shrink
            x = 1
            y=0
            rotate -= .4
        elif pygame.key.get_pressed()[K_DOWN]: #Enter to pause scale and rotation
            x = 1
            y = 0
            rotate += .4
        elif pygame.key.get_pressed()[K_r]:
            menu()
        ### END KEY INPUTS

        glRotatef(rotate, x, y, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glScalef(scale, scale, scale)
        glColor(0,0,1)
        draw_shape(edges_cube, vertices_cube)
        pygame.display.flip()
        clock.tick(60)

    ###SPHERE MODE###
def sphere_playground():
    """
    Displays the full playground game mode for the sphere
    The sphere is made up of four quadrants, one being blue, then red, then green, then purple
    The user cannot see through this shape as they can with the diamond and cube
    User can press keys to play with sphere:
    1 = grow
    2 = shrink
    Right = Spin right
    Left = Spin left
    Up = Spin up
    Down = Spin down
    Return = stop scaling and rotation
    Click on screen = cube moves to click location (depends on rotation)
    R = return to menu
    """
    ###3D INITIALIZING###
    pygame.display.set_mode((WIDTH, HEIGHT),DOUBLEBUF | OPENGL)  # Double buffering visuals and enable OpenGl to run in pygame window
    ##SET UP SCREEN FOR 3D
    gluPerspective(45, ((WIDTH, HEIGHT)[0] / (WIDTH, HEIGHT)[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    #CREATE QUADRIC FOR SPHERE
    quadrie = gluNewQuadric()
    gluQuadricDrawStyle(quadrie, GLU_FILL)
    gluQuadricNormals(quadrie, GL_SMOOTH)

    #INITIALizE GRAPHICS
    glEnable(GL_DEPTH_TEST) #DEPTH TEST FIXED EVERYTHING THANK THE HEAVENS. MAKES IT TO THAT SPHERE VISUALLY ROTATES
    glEnable(GL_LIGHTING) #CREATE LIGHTING
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (.5, .5, .5, 1.0)) #MAKE LIGHTING BRIGHT AND TOUCH ALL PARTS OF SPHERE FOR BEST VISION
    glEnable(GL_COLOR_MATERIAL) #CREATE MATERIAL SO THAT LIGHT SHOWS OFF COLOR
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    scale = 1  # No Scaling Base Variable
    rotate = 0  # Slow Rotation Base variable (CHANGE THIS TO NO ROTATION?)
    numerate = 0 #Find number of times mouse is clicked for movement

    ### START GRAPHICS LOOP ###
    x, y = 1, 0
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            ###MOVE SPHERE TO WHERE USER PRESSES###
            if event.type == pygame.MOUSEBUTTONDOWN:
                # MOVEMENT WILL BE MESSED UP IF USER STARTS ROTATION
                numerate += 1
                move_shape(numerate)
        if pygame.key.get_pressed()[K_1]: #1 to scale up
            scale += .001
        elif pygame.key.get_pressed()[K_2]: #2 to shrink
            scale -= .001
        elif pygame.key.get_pressed()[K_RETURN]: #Enter to pause scale and rotation
            scale = 1
            rotate = 0
        elif pygame.key.get_pressed()[K_RIGHT]: #3 to rotate right
            x = 0
            y = 1
            rotate += .4
        elif pygame.key.get_pressed()[K_LEFT]: #4 to rotate left
            x = 0
            y = 1
            rotate -= .4
        elif pygame.key.get_pressed()[K_UP]:
            #2 to shrink
            x = 1
            y=0
            rotate -= .4
        elif pygame.key.get_pressed()[K_DOWN]: #Enter to pause scale and rotation
            x = 1
            y = 0
            rotate += .4
        elif pygame.key.get_pressed()[K_r]: #r to return to the menu
            menu()

        text_surface = FONT.render('3D PLAYGROUND', True, (100, 0, 0))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(rotate, x, y, 0)
        draw_sphere(quadrie)
        glScalef(scale, scale, scale) #Change scale based on user inputs from before
        pygame.display.flip()
        clock.tick(60)
def main():
    menu()

main()
