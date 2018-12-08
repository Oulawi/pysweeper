import pygame
from random import randint

class Square:
    def __init__(self, xcoor, ycoor):
        self.status = randint(10, 11)
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
        return 'Square at ({}, {}) status {}'.format(self.xcoor, self.ycoor, self.status)

    def __repr__(self):
        return 'Square({}, {})'.format(self.xcoor, self.ycoor)


        


class Grid:
    def __init__(self):
        self.gridx = 24
        self.gridy = 24
        self.squares = set()

        for j in range(0, self.gridy):
            for i in range(0, self.gridx):
                self.squares.add(Square(i,j))

    def set_states(self):
        pass

#Game loop

pygame.init()
pygame.mixer.quit()
pygame.display.set_caption("Othello")

clock = pygame.time.Clock()
tickrate = 20

grid = Grid()
grid.set_states()
width = grid.gridx*40 + (grid.gridx - 1)*4
heigth = grid.gridy*40 + (grid.gridy - 1)*4
screen = pygame.display.set_mode((width, heigth))


done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill([180, 180, 180])
    for i in range(0, grid.gridx):
        pygame.draw.rect(screen, [0,0,0], pygame.Rect(40 * i + 4 * i, 0, 4, grid.gridx*40 + (grid.gridx -1)*4))
    for i in range(0, grid.gridy):
        pygame.draw.rect(screen, [0,0,0], pygame.Rect(0, 40 * i + 4 * i, grid.gridx*40 + (grid.gridx -1)*4, 4))

    for i in grid.squares:
        if i.status == 11:
            pygame.draw.circle(screen, (255,0,0), (i.xcoor*40 + 23 + i.xcoor*4, i.ycoor*40 + 23 + i.ycoor*4), 15)
    
    pygame.display.update()
    pygame.display.flip()
    clock.tick(tickrate)

if pygame.image.get_extended:
    print("True")
else:
    print("Oh no")

pygame.quit()