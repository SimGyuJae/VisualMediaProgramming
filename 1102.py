import pygame
import numpy as np

RED = (255, 0, 0)

FPS = 60   # frames per second

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

def CirclesOverlap (c1, c2):
    dist12 = np.sqrt( (c1.position[0] - c2.position[0])**2 + (c1.position[1] - c2.position[1])**2 )
    if dist12 < c1.radius + c2.radius:
        return True # if overlaps
    return False

class MyCircle():
    def __init__(self, x, y, vx, vy, radius=40, color=None, sound = None):
        self.radius = radius 
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy 
        self.ax = 0
        self.ay = .1
        self.org_color = color if color is not None else (100, 200, 255)
        self.color = self.org_color
        self.sound = sound
        return
    
    def update(self):
        
        self.x = self.x + self.vx 
        if self.x + self.radius >= WINDOW_WIDTH:
            self.vx = -1. * self.vx 
        if self.x - self.radius < 0:
            self.vx = -1. * self.vx 

        self.y = self.y + self.vy
        self.vy = self.vy + self.ay 
        if self.y < 0:
            self.vy = 0
            self.y = self.radius + 10
        if self.y + self.radius >= WINDOW_HEIGHT:
            self.vy = -1 * self.vy 
            if self.sound is not None:
                # self.sound.play()
                pass
        return
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           [self.x, self.y], 
                           radius = self.radius, )

    def print(self,):
        print("my class self.number = ", self.number)
        return
# 

def getRegularPolygon(nV, radius=1.):
    angle_step = 360. / nV 
    half_angle = angle_step / 2.

    vertices = []
    for k in range(nV):
        degree = angle_step * k 
        radian = np.deg2rad(degree + half_angle)
        x = radius * np.cos(radian)
        y = radius * np.sin(radian)
        vertices.append( [x, y] )
    #
    print("list:", vertices)

    vertices = np.array(vertices)
    print('np.arr:', vertices)
    return vertices



class myTriangle():
    def __init__(self, radius=50, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.vertices = getRegularPolygon(3, radius=self.radius)

        self.color = color

        self.angle = 0.
        self.angvel = np.random.normal(5., 7)

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
        self.angle += self.angvel
        self.position += self.vel

        if self.position[0] >= WINDOW_WIDTH:
            self.vel[0] = -1. * self.vel[0]

        if self.position[0] < 0:
            self.vel[0] *= -1.

        if self.position[1] >= WINDOW_HEIGHT:
            self.vel[1] *= -1.

        if self.position[1] < 0:
            self.vel[1] *= -1

        # print(self.tick, self.position)

        return

    def draw(self, screen):
        R = Rmat(self.angle)
        points = self.vertices @ R.T + self.position
        pygame.draw.polygon(screen, self.color, points)
#

class myPolygon():
    def __init__(self, nvertices = 3, radius=70, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.nvertices = nvertices
        self.vertices = getRegularPolygon(self.nvertices, radius=self.radius)

        self.color = color
        self.color_org = color 

        self.angle = 0.
        self.angvel = np.random.normal(5., 7)

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
        self.angle += self.angvel
        self.position += self.vel

        if self.position[0] >= WINDOW_WIDTH:
            self.vel[0] = -1. * self.vel[0]

        if self.position[0] < 0:
            self.vel[0] *= -1.

        if self.position[1] >= WINDOW_HEIGHT:
            self.vel[1] *= -1.

        if self.position[1] < 0:
            self.vel[1] *= -1

        # print(self.tick, self.position)

        return

    def draw(self, screen):
        R = Rmat(self.angle)
        points = self.vertices @ R.T + self.position

        pygame.draw.polygon(screen, self.color, points)
#

def update_list(alist):
    for a in alist:
        a.update()
#
def draw_list(alist, screen):
    for a in alist:
        a.draw(screen)
#

def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation
#

def draw(P, H, screen, color=(100, 200, 200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T 
    pygame.draw.polygon(screen, color=color, 
                        points=Ptransformed, width=3)
    return
#


def main():
    pygame.init() # initialize the engine

    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    w = 200
    h = 40
    X = np.array([ [0,0], [w, 0], [w, h], [0, h] ])
    gw = 60
    gh = 20
    G = np.array([ [0,0], [gw, 0], [gw, gh], [0, gh] ])
    position = [WINDOW_WIDTH/2, WINDOW_HEIGHT - 100]
    keyboard_x = 0
    keyboard_arm1 = 0
    keyboard_arm2 = 0
    keyboard_arm3 = 0
    keyboard_grap = 0
    keyboard_dx = 0
    keyboard_darm1 = 0
    keyboard_darm2 = 0
    keyboard_darm3 = 0
    tick = 0
    done = False
    while not done:
        tick += 1
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # 키가 눌릴 경우
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keyboard_dx = -1
                elif event.key == pygame.K_RIGHT:
                    keyboard_dx = 1

                elif event.key == pygame.K_q:
                    keyboard_darm1 = -1
                elif event.key == pygame.K_w:
                    keyboard_darm1 = 1

                elif event.key == pygame.K_a:
                    keyboard_darm2 = -1
                elif event.key == pygame.K_s:
                    keyboard_darm2 = 1

                elif event.key == pygame.K_z:
                    keyboard_darm3 = -1
                elif event.key == pygame.K_x:
                    keyboard_darm3 = 1

                elif event.key == pygame.K_SPACE:
                    keyboard_grap = -25
                        
        
        # 키가 놓일 경우
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    keyboard_dx = 0
                elif event.key == pygame.K_q or event.key == pygame.K_w:
                    keyboard_darm1 = 0
                elif event.key == pygame.K_a or event.key == pygame.K_s:
                    keyboard_darm2 = 0
                elif event.key == pygame.K_z or event.key == pygame.K_x:
                    keyboard_darm3 = 0
                elif event.key == pygame.K_SPACE:
                    keyboard_grap = 0
                    
        # drawing
        screen.fill( (200, 254, 219))
        keyboard_x += keyboard_dx
        keyboard_arm1 += keyboard_darm1
        keyboard_arm2 += keyboard_darm2
        keyboard_arm3 += keyboard_darm3
        
        # base, 좌우 화살표
        pygame.draw.circle(screen, (255,0,0), position, radius=3)
        H0 = Tmat(position[0], position[1]) @ Tmat(0 + keyboard_x, -h)
        draw(X, H0, screen, (0,0,0)) # base

        # arm 1, q w 키
        H1 = H0 @ Tmat(w/2, 0)  
        x, y = H1[0,2], H1[1,2] # joint position
        H11 = H1 @ Rmat(-90) @ Tmat(0,-h/2)
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H12 = H11 @ Tmat(0, h/2) @ Rmat(keyboard_arm1) @ Tmat(0, -h/2)    
        draw(X, H12, screen, (200,200,0)) # arm 1, 90 degree

        # arm 2, a s 키
        H2 = H12 @ Tmat(w, 0) @ Tmat(0, h/2) 
        x, y = H2[0,2], H2[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H21 = H2 @ Rmat(keyboard_arm2) @ Tmat(0, -h/2)
        draw(X, H21, screen, (0,0, 200))

        # arm 3, z x 키
        H3 = H21 @ Tmat(w, 0) @ Tmat(0, h/2) 
        x, y = H3[0,2], H3[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H31 = H3 @ Rmat(keyboard_arm3) @ Tmat(0, -h/2)
        draw(X, H31, screen, (0,0, 200))

        # grip
        G1 = H31 @ Tmat(w, 0) @ Tmat(0, h/2) 
        x, y = G1[0,2], G1[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        G11 = G1 @ Rmat(90) @ Tmat(-gw/2, -gh)#
        draw(G, G11, screen, (0,0, 200))
        
        # grap right
        G2 = G11 @ Tmat(gw, 0) @ Tmat(0, gh/2) 
        G21 = G2 @ Rmat(90) @ Tmat(-gw, -gh -keyboard_grap)
        draw(G, G21, screen, (0,0, 200))

         # grap left
        G3 = G11 @ Tmat(gw, 0) @ Tmat(0, gh/2) 
        G31 = G3 @ Rmat(90) @ Tmat(-gw, 3 * gh + keyboard_grap)
        draw(G, G31, screen, (0,0, 200))

        # finish
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()