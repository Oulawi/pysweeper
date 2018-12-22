import pygame
from random import randint

class Square:
    def __init__(self, xcoor, ycoor):
        self.is_bomb = 0
        self.is_open = 0
        self.nearby_bombs = 0
        self.xcoor = xcoor
        self.ycoor = ycoor
    
    def __eq__(self, other):
        if self.xcoor == other.xcoor and self.ycoor == other.ycoor:
            return True
        else:
            return False
        
    def __hash__(self):
        hashvalue = self.xcoor + self.ycoor**2
        return hashvalue

    def __str__(self):
        return 'Square at ({}, {}) bomb: {}'.format(self.xcoor, self.ycoor, self.is_bomb)

    def __repr__(self):
        return 'Square({}, {})[{}]'.format(self.xcoor, self.ycoor, self.is_bomb)

    def neighbours(self):
        neighbours = set()
        for j in range(self.ycoor - 1, self.ycoor + 2):
            for i in range(self.xcoor - 1, self.xcoor + 2):
                if i != self.xcoor or j != self.ycoor:
                    neighbours.add(Square(i, j))
        return neighbours

class Grid:
    def __init__(self):
        self.gridx = 24
        self.gridy = 24
        self.squares = set()

        for j in range(0, self.gridy):
            for i in range(0, self.gridx):
                self.squares.add(Square(i,j))

        mines = []
        for i in range (0, 99):
            while True:
                minex = randint(0,23)
                miney = randint(0,23)
                if (minex, miney) not in mines:
                    mines.append((minex, miney))
                    break
        for i in mines:
            for j in self.squares:
                if i[0] == j.xcoor and i[1] == j.ycoor:
                    j.is_bomb = 1

        for i in self.squares:
            if i.is_bomb == 1:
                None
            else:
                neighbouring_bombs = 0
                neighbours = self.squares.intersection(i.neighbours())
                for s in self.squares:
                    if s in neighbours and s.is_bomb == 1:
                        neighbouring_bombs += 1
                i.nearby_bombs = neighbouring_bombs



#Game loop

pygame.init()
pygame.mixer.quit()
pygame.display.set_caption("PySweeper")

clock = pygame.time.Clock()
tickrate = 20

grid = Grid()
width = grid.gridx*40 + (grid.gridx - 1)*4
heigth = grid.gridy*40 + (grid.gridy - 1)*4
screen = pygame.display.set_mode((width, heigth))

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill([200, 200, 200])
    for i in range(0, grid.gridx):
        pygame.draw.rect(screen, [0,0,0], pygame.Rect(40 * i + 4 * i, 0, 4, grid.gridx*40 + (grid.gridx -1)*4))
    for i in range(0, grid.gridy):
        pygame.draw.rect(screen, [0,0,0], pygame.Rect(0, 40 * i + 4 * i, grid.gridx*40 + (grid.gridx -1)*4, 4))

    for i in grid.squares:
        if i.is_bomb == 1:
            pygame.draw.circle(screen, (255,0,0), (i.xcoor*40 + 23 + i.xcoor*4, i.ycoor*40 + 23 + i.ycoor*4), 15)
        elif i.nearby_bombs == 1:
            pygame.draw.circle(screen, (0,0,200), (i.xcoor*40 + 23 + i.xcoor*4, i.ycoor*40 + 23 + i.ycoor*4), 15)

    
    pygame.display.update()
    pygame.display.flip()
    clock.tick(tickrate)

pygame.quit()