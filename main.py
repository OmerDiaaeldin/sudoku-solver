import pygame
# import main
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
    def edit(self, val):
        if self.solid:
            return
        numbers = [str(x) for x in range(1, 10)]
        print(val)
        if val in numbers:
            self.value = val
            self.text_pos = (self.col*self.side, self.row*self.side)
            self.text_color = (200,200,200)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.col*self.side, self.row*self.side, self.side,self.side),self.line_width)
        if(self.value == 0):
            return
        font = pygame.font.Font('freesansbold.ttf', 32)
        text_surface = font.render(str(self.value), True, self.text_color)
        screen.blit(text_surface, self.text_pos)
        # pygame.display.flip()

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
    def get_patch(self, pos):
        """ takes the position and returns the patch coordinates"""
        return (pos[1]//self.patch_side, pos[0]//self.patch_side)
    def edit(self, val):
        if(not self.highlighted_patch):
            return
        row, col = self.highlighted_patch
        patch = self.patches[row][col]
        patch.edit(val)

    def highlight(self, pos):
        if(self.highlighted_patch):
            row, col = self.highlighted_patch
            self.patches[row][col].un_highlight()
        self.highlighted_patch = self.get_patch(pos)
        self.patches[self.highlighted_patch[0]][self.highlighted_patch[1]].highlight()
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
            grid.edit(chr(event.key))
    screen.fill((255,255,255))
    grid.draw(screen)
    pygame.display.flip()