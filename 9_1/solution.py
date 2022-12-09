#!/bin/python3

from parser import Parser

Debug = False

class Cell:
  def __init__(self):
    self.visitedByTail = False

class ObjectPosition:
  def __init__(self, x, y):
    self.X = x
    self.Y = y

class DynamicGrid:
  def __init__(self):
    self.head = ObjectPosition(0,0)
    self.tail = ObjectPosition(0,0)
    self.currentWidth = 1
    self.currentHeight = 1
    # initialize 1-by-1 grid with a visited cell
    cell = Cell()
    cell.visitedByTail = True
    self.grid = [[cell]]
  
  def moveHead(self, direction, amount):
    i = 0
    while i < int(amount):
      self.step(direction)
      i += 1

  def addRowAbove(self):
    newRow = []
    i = 0
    while i < self.currentWidth:
      newRow.append(Cell())
      i += 1
    self.grid.insert(0, newRow)
    self.currentHeight += 1

  def addRowBelow(self):
    newRow = []
    i = 0
    while i < self.currentWidth:
      newRow.append(Cell())
      i += 1
    self.grid.append(newRow)
    self.currentHeight += 1
    self.head.Y += 1
    self.tail.Y += 1

  def addColumnLeft(self):
    for line in self.grid:
      line.insert(0, Cell())
    self.currentWidth += 1
    self.head.X += 1
    self.tail.X += 1

  def addColumnRight(self):
    for line in self.grid:
      line.append(Cell())
    self.currentWidth += 1

  def stepUp(self):
    # if we're already at the edge we need to dynamically insert a row
    if self.head.Y == self.currentHeight - 1:
      self.addRowAbove()
    self.head.Y += 1

  def stepDown(self):
    # if we're already at the edge we need to dynamically insert a row
    if self.head.Y == 0:
      self.addRowBelow()
    self.head.Y -= 1

  def stepLeft(self):
    # if we're already at the edge we need to dynamically insert a row
    if self.head.X == 0:
      self.addColumnLeft()
    self.head.X -= 1

  def stepRight(self):
    # if we're already at the edge we need to dynamically insert a row
    if self.head.X == self.currentWidth - 1:
      self.addColumnRight()
    self.head.X += 1

  def updateTailCellStatus(self):
    if Debug:
      print(f"current head position [{self.head.X},{self.currentHeight-self.head.Y-1}]")
      print(f"updating cell status at [{self.tail.X},{self.currentHeight-self.tail.Y-1}]")
    self.grid[self.currentHeight-self.tail.Y-1][self.tail.X].visitedByTail = True

  def updateTail(self):
    # are H and T touching? if so no need to update
    if (self.head.X <= self.tail.X+1 and self.head.X >= self.tail.X-1) and (self.head.Y <= self.tail.Y+1 and self.head.Y >= self.tail.Y-1):
      return

    # they are not touching, are they in the same row or column?
    if self.head.Y == self.tail.Y:
      # need to move tail left or right?
      if self.head.X < self.tail.X:
        # move left
        self.tail.X -= 1
      else:
        self.tail.X += 1
    elif self.head.X == self.tail.X:
      # need to move tail up or down?
      if self.head.Y < self.tail.Y:
        # move down
        self.tail.Y -= 1
      else:
        self.tail.Y += 1
    else:
      # now we have to move diagonally
      x_mod = -1 if self.head.X < self.tail.X else 1
      y_mod = -1 if self.head.Y < self.tail.Y else 1
      self.tail.X += x_mod
      self.tail.Y += y_mod
    self.updateTailCellStatus()

  def step(self, direction):
    if direction == 'U':
      self.stepUp()
    elif direction == 'D':
      self.stepDown()
    elif direction == 'L':
      self.stepLeft()
    elif direction == 'R':
      self.stepRight()
    self.updateTail()


tokenDefinitions = {
  "direction": "[LRUD]",
  "number": "([0-9])+",
}

grammarRules = {
  "moveset": "(moveInstruction)+",
  "moveInstruction": "direction=t:direction amount=t:number <move>",
}

dynamicGrid = DynamicGrid()

actions = {
  "move": lambda context : dynamicGrid.moveHead(context["direction"], context["amount"]),
}

f = open("input.txt", "r")
parser = Parser(tokenDefinitions, grammarRules, actions, "moveset", f.readlines(), 1)
parser.parse()

count = 0
for line in dynamicGrid.grid:
  for cell in line:
    if cell.visitedByTail:
      count += 1

print(count)