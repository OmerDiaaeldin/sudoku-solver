import pygame
import datetime as dt
from solver import valid, solve_board
class Patch(pygame.sprite.Sprite):
    def __init__(self, side, row, col, value, solid = True, penciled=False):
        pygame.sprite.Sprite.__init__(self)
        self.solid = solid
        self.value = value
        self.side = side
        self.row = row
        self.col = col
        self.penciled = penciled
        self.color = (0,0,0)
        self.line_width = 1
        self.text_pos = (self.col*self.side + self.side//4, self.row*self.side + self.side//4)
        self.text_color = (0,0,0)
    def highlight(self):
        self.color = (255,0,0)
        self.line_width = 2
    def un_highlight(self):
        self.color = (0,0,0)
        self.line_width = 1

    def confirm(self):
        self.text_pos = (self.col*self.side + self.side//4, self.row*self.side + self.side//4)
        self.text_color = (0, 0, 200)
    def edit(self, event):
        """return 0, if nothing changed, 1 if added value, 2 if deleted value"""
        if self.solid:
            return
        old_value = self.value
        if event.key == pygame.K_BACKSPACE:
            self.value = 0
            if(old_value != 0):
                return 2
            return 0
        val = chr(event.key)
        numbers = [str(x) for x in range(1, 10)]
        if val in numbers:
            self.value = int(val)
            self.text_pos = (self.col*self.side, self.row*self.side)
            self.text_color = (200,200,200)
            if(old_value == 0):
                return 1
            return 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.col*self.side, self.row*self.side, self.side,self.side),self.line_width)
        if(self.value == 0):
            return
        font = pygame.font.Font('freesansbold.ttf', 32)
        text_surface = font.render(str(self.value), True, self.text_color)
        screen.blit(text_surface, self.text_pos)
        # pygame.display.flip()

class Clock(pygame.sprite.Sprite):
    def __init__(self, patch_size):
        self.datetime = dt.datetime.now()
        self.patch_size = patch_size
    def get_time(self):
        return dt.datetime.now()-self.datetime

    def draw(self, screen):
        time = self.get_time()
        seconds = time.seconds
        hours = time.seconds//3600
        minutes = (seconds-hours*3600) // 60
        seconds = seconds - hours*3600 - minutes*60

        font = pygame.font.SysFont('DS-Digital', 32)
        text_surface = font.render(f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}", True,(0,0,0))
        screen.blit(text_surface, (self.patch_size*4, self.patch_size*9))

class Grid(pygame.sprite.Sprite):
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 3, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    def __init__(self, patch_side=60):
        pygame.sprite.Sprite.__init__(self)
        self.patch_side = patch_side
        self.patches = [[Patch(self.patch_side,i,j,self.board[i][j]) for j in range(9)] for i in range(9)]
        self.highlighted_patch = None
        for i in range(9):
            for j in range(9):
                if(self.patches[i][j].value == 0):
                    self.patches[i][j].solid = False
        self.penciled = []
        self.clock = Clock(self.patch_side)
    def get_patch(self, pos):
        """ takes the position and returns the patch coordinates"""
        return (pos[1]//self.patch_side, pos[0]//self.patch_side)
    def confirm_additions(self):
        """return True if the additions are valid otherwise false. delete the penciled entires anyway"""
        affirm = True
        for coordinates in self.penciled:
            if not valid(self.patches, self.patches[coordinates[0]][coordinates[1]].value, coordinates):
                affirm = False
                break

        if(affirm):
            for coordinates in self.penciled:
                self.patches[coordinates[0]][coordinates[1]].confirm()
        else:
            for coordinates in self.penciled:
                self.patches[coordinates[0]][coordinates[1]].value = 0

        for coordinates in self.penciled:
            self.penciled.remove(coordinates)
    def edit(self, event):
        if(event.key == pygame.K_c):
            self.confirm_additions()
            return
        if(event.key == pygame.K_s):
            self.solution()
            return
        if(not self.highlighted_patch):
            return
        row, col = self.highlighted_patch
        patch = self.patches[row][col]
        status = patch.edit(event)
        if(status == 1):
            self.penciled.append((row, col))
        elif(status == 2):
            self.penciled.remove((row, col))

    def highlight(self, pos):
        if(self.highlighted_patch):
            row, col = self.highlighted_patch
            self.patches[row][col].un_highlight()
        self.highlighted_patch = self.get_patch(pos)
        self.patches[self.highlighted_patch[0]][self.highlighted_patch[1]].highlight()
    def solution(self):
        # erase all the values by the user and solve from scratch
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.patches[i][j].color = (0,0,0)
                self.patches[i][j].text_color = (0, 0, 0)
                self.patches[i][j].color = (0, 0, 0)
                if(not self.patches[i][j].solid):
                    self.patches[i][j].value = 0
        solve_board(self.patches)
        print("DONE!!!")

    def draw(self, screen):
        dim = screen.get_width()
        pygame.draw.line(screen, (0,0,0), (0, dim/3), (dim,dim/3), 4)
        pygame.draw.line(screen, (0,0,0), (0, 2*dim/3), (dim,2*dim/3), 4)
        pygame.draw.line(screen, (0,0,0), (dim/3,0), (dim/3, dim), 4)
        pygame.draw.line(screen, (0,0,0), (2*dim/3, 0), (2*dim/3, dim), 4)
        pygame.draw.rect(screen, (0,0,0), pygame.rect.Rect(0, 0, dim, dim),1)
        for i in range(9):
            for j in range(9):
                self.patches[i][j].draw(screen)
        self.clock.draw(screen)

pygame.init()
screen = pygame.display.set_mode((540,600))
pygame.display.set_caption('Sudoku solver')
grid = Grid()

running = True
while(running):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid.highlight(event.pos)
        if event.type == pygame.KEYDOWN:
            grid.edit(event)
    screen.fill((255,255,255))
    grid.draw(screen)
    pygame.display.flip()