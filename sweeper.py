import pygame
from random import randint

class Square:
    def __init__(self, xcoor, ycoor):
        self.is_bomb = 0
        self.is_open = False
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

class Selectionner:
    def __init__(self, xcoor, ycoor):
        self.xcoor = xcoor
        self.ycoor = ycoor
        self.trigger = False
    
    def move_selection(self, direction):
        if direction == 'up':
            self.ycoor -= 1
        elif direction == 'right':
            self.xcoor += 1
        elif direction == 'down':
            self.ycoor += 1
        elif direction == 'left':
            self.xcoor -= 1

    def draw_selection(self, colour):
        pygame.draw.rect(screen, colour, pygame.Rect(self.xcoor*40 + self.xcoor*4, self.ycoor*40 + self.ycoor*4, 48, 4))
        pygame.draw.rect(screen, colour, pygame.Rect(self.xcoor*40 + self.xcoor*4, self.ycoor*40 + self.ycoor*4 + 44, 48, 4))
        pygame.draw.rect(screen, colour, pygame.Rect(self.xcoor*40 + self.xcoor*4, self.ycoor*40 + self.ycoor*4, 4, 48))
        pygame.draw.rect(screen, colour, pygame.Rect(self.xcoor*40 + self.xcoor*4 + 44, self.ycoor*40 + self.ycoor*4, 4, 48))



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
player = Selectionner(2,2)
done = False
held_down = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        print("Triggered!!!")
        player.trigger = True
    elif pressed[pygame.K_UP] and held_down != True:
        player.move_selection('up')
        held_down = True
    elif pressed[pygame.K_DOWN] and held_down != True:
        player.move_selection('down')
        held_down = True
    elif pressed[pygame.K_LEFT] and held_down != True:
        player.move_selection('left')
        held_down = True
    elif pressed[pygame.K_RIGHT] and held_down != True:
        player.move_selection('right')
        held_down = True
    elif not (pressed[pygame.K_UP] or pressed[pygame.K_DOWN] or pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]):
        held_down = False



    screen.fill([200, 200, 200])
    for i in range(0, grid.gridx):
        pygame.draw.rect(screen, [0,0,0], pygame.Rect(40 * i + 4 * i, 0, 4, grid.gridx*40 + (grid.gridx -1)*4))
    for i in range(0, grid.gridy):
        pygame.draw.rect(screen, [0,0,0], pygame.Rect(0, 40 * i + 4 * i, grid.gridx*40 + (grid.gridx -1)*4, 4))

    for i in grid.squares:
        if player.trigger:
            print("HELLO")
            if i.xcoor == player.xcoor and i.ycoor == player.ycoor:
                i.is_open = True
        if i.is_open:
            if i.is_bomb == 1:
                image = pygame.image.load_basic('mine.bmp')
                screen.blit(image, (40*i.xcoor + 4*(i.xcoor + 1), 40*i.ycoor + 4*(i.ycoor + 1)))
            elif i.nearby_bombs == 0:
                None
            else:
                image = pygame.image.load_basic('number{}.bmp'.format(i.nearby_bombs))
                screen.blit(image, (40*i.xcoor + 4*(i.xcoor + 1), 40*i.ycoor + 4*(i.ycoor + 1)))
    
    player.draw_selection((255, 255, 0))
            


    
    pygame.display.update()
    pygame.display.flip()
    player.trigger = False
    clock.tick(tickrate)

pygame.quit()