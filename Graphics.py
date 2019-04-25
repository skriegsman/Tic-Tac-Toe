import sys
import pygame
import Constants
from Constants import consts
from pygame.locals import QUIT

class PygameScreen:
    def __init__(self):
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((consts.WINDOWWIDTH, consts.FULLWINDOWHEIGHT))
        self.FPSCLOCK = pygame.time.Clock()

        self.compute_specs()
        font_size = min([consts.WINDOWWIDTH // 30, 18])
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', font_size)
        pygame.display.set_caption('Tic-Tac-Toe')

        self.mark_history = []
        self.draw()

    def reset(self):
        self.mark_history = []
        self.draw()

    def _make_rect(self, i, j):

        x = self.CELLSIZE[0]*i + self.OFFSET[0]
        y = self.CELLSIZE[1]*j + self.OFFSET[1]
        w = self.CELLSIZE[0] - 2 * self.OFFSET[0]
        h = self.CELLSIZE[1] - 2 * self.OFFSET[1]

        return pygame.Rect(x, y, w, h)

    def compute_specs(self):
        self.CELLSIZE = (consts.WINDOWWIDTH//3, consts.WINDOWHEIGHT//3)
        self.OFFSET = (self.CELLSIZE[0]//10, self.CELLSIZE[1]//10)
        self.RECTS = [[self._make_rect(col_i, row_j) for col_i in range(3)] for row_j in range(3)]

    def draw(self, move=None, player=None):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()

        self.DISPLAYSURF.fill(consts.BGCOLOR)
        self.draw_grid()
        self.draw_menu()
        if player and move:
            new_mark = {"coords":move, "player":str(player)}
            self.mark_history.append(new_mark)
        for mark in self.mark_history:
            self.draw_mark(mark)
        pygame.display.update()
        self.FPSCLOCK.tick(consts.FPS)

    def draw_grid(self):
        for i in range(1,3):
            #Vertical Grid Lines
            pygame.draw.line(self.DISPLAYSURF, consts.BLACK, ((consts.WINDOWWIDTH // 3)*i, 0), ((consts.WINDOWWIDTH // 3)*i, consts.WINDOWHEIGHT),3)
            #Horizontal Grid Lines
            pygame.draw.line(self.DISPLAYSURF, consts.BLACK, (0, (consts.WINDOWHEIGHT // 3)*i), (consts.WINDOWWIDTH, consts.WINDOWHEIGHT // 3*i), 3)

    def draw_menu(self):
        pygame.draw.rect(self.DISPLAYSURF, consts.LIGHTBLUE, (0,consts.WINDOWHEIGHT,consts.WINDOWWIDTH,consts.MENUHEIGHT), 0)
        pygame.draw.rect(self.DISPLAYSURF, consts.BLACK, (0,consts.WINDOWHEIGHT,consts.WINDOWWIDTH,consts.MENUHEIGHT), 3)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

    def draw_mark(self, mark):
        if mark['player'] == consts.X:
            self.draw_x(mark['coords'])
        else:
            self.draw_o(mark['coords'])

    def draw_x(self, mark_coords):
        i, j = mark_coords
        rect = self.RECTS[i][j]
        pygame.draw.line(self.DISPLAYSURF, consts.RED, rect.topleft, rect.bottomright, consts.XWIDTH)
        pygame.draw.line(self.DISPLAYSURF, consts.RED, rect.bottomleft, rect.topright, consts.XWIDTH)

    def draw_o(self, mark_coords):
        i, j = mark_coords
        rect = self.RECTS[i][j]
        center = rect.center
        radius = rect.width // 2
        radius -= radius//3
        pygame.draw.circle(self.DISPLAYSURF, consts.BLUE, center, radius, radius//3)

    def getMouseMove(self):
        notClick = True
        while(notClick):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if x < (consts.WINDOWWIDTH/3):
                        if y < (consts.WINDOWHEIGHT/3): return (0,0)
                        elif y > 2*(consts.WINDOWHEIGHT/3): return (2,0)
                        else: return (1,0)
                    elif x > 2*(consts.WINDOWWIDTH/3):
                        if y < (consts.WINDOWHEIGHT/3): return (0,2)
                        elif y > 2*(consts.WINDOWHEIGHT/3): return (2,2)
                        else: return (1,2)
                    else:
                        if y < (consts.WINDOWHEIGHT/3): return (0,1)
                        elif y > 2*(consts.WINDOWHEIGHT/3): return (2,1)
                        else: return (1,1)
                    notClick = False

    def terminate(self):
        pygame.quit()
        sys.exit()
