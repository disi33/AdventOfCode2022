#!/bin/python3

from enum import Enum

class Direction(Enum):
  NORTH = 1,
  EAST = 2,
  SOUTH = 3,
  WEST = 4

all_directions = [
  Direction.NORTH,
  Direction.EAST,
  Direction.SOUTH,
  Direction.WEST
]

Debug = False

class ForestMap:
  def __init__(self, lines):
    self.forestWidth = len(lines[0].strip())
    self.forestHeight = len(lines)
    self.forestGrid = []
    self.visibilityMap = {}
    self.initializeVisibilityMap()
    self.initializeForestGrid(lines)
    self.checkVisibility()

  def initializeVisibilityMap(self):
    for direction in all_directions:
      self.visibilityMap[direction] = self.createDefaultVisibilityMap(0)

  def createDefaultVisibilityMap(self, initializor = 1):
    newMap = []
    i = 0
    while i < self.forestHeight:
      newRow = []
      j = 0
      while j < self.forestWidth:
        newRow.append(initializor)
        j += 1
      i += 1
      newMap.append(newRow)
    return newMap

  def initializeForestGrid(self, lines):
    for line in lines:
      newRow = []
      for num in line.strip():
        newRow.append(int(num))
      self.forestGrid.append(newRow)

  def getHorizontalViewingDistance(self, x, y, direction):
    if Debug:
      print(f"calculating distance in direction {direction} for value {self.forestGrid[y][x]} [{x},{y}]")
    distance = 0
    if direction == Direction.EAST:
      startIndex = x+1
      endIndex = self.forestWidth
      increment = 1
    else:
      startIndex = x-1
      endIndex = -1
      increment = -1

    x_i = startIndex
    while x_i != endIndex:
      distance += 1

      if Debug:
        print(f"  - comparing with value {self.forestGrid[y][x_i]} [{x_i},{y}]")
      if self.forestGrid[y][x_i] >= self.forestGrid[y][x]:
        break
      x_i += increment

    if Debug:
      print(f"  - calculated distance {distance}")
    
    return distance

  def getVerticalViewingDistance(self, x, y, direction):
    if Debug:
      print(f"calculating distance in direction {direction} for value {self.forestGrid[y][x]} [{x},{y}]")
    distance = 0
    if direction == Direction.NORTH:
      startIndex = y-1
      endIndex = -1
      increment = -1
    else:
      startIndex = y+1
      endIndex = self.forestHeight
      increment = 1

    y_i = startIndex
    while y_i != endIndex:
      distance += 1
      if self.forestGrid[y_i][x] >= self.forestGrid[y][x]:
        break
      y_i += increment
    
    return distance


  def checkVisibilityHorizontally(self, direction):
    startIndex = None
    endIndex = None
    increment = None
    if direction == Direction.EAST:
      startIndex = 0
      endIndex = self.forestWidth
      increment = 1
    else:
      startIndex = self.forestWidth -1
      endIndex = -1
      increment = -1

    rowIndex = 0
    while rowIndex < self.forestHeight:
      searchIndex = startIndex
      while searchIndex != endIndex:
        self.visibilityMap[direction][rowIndex][searchIndex] = self.getHorizontalViewingDistance(searchIndex, rowIndex, direction)
        searchIndex += increment
      rowIndex += 1

  def checkVisibilityVertically(self, direction):
    startIndex = None
    endIndex = None
    increment = None
    if direction == Direction.SOUTH:
      startIndex = 0
      endIndex = self.forestHeight
      increment = 1
    else:
      startIndex = self.forestHeight-1
      endIndex = -1
      increment = -1

    columnIndex = 0
    while columnIndex < self.forestWidth:
      searchIndex = startIndex
      while searchIndex != endIndex:
        self.visibilityMap[direction][searchIndex][columnIndex] = self.getVerticalViewingDistance(columnIndex, searchIndex, direction)
        searchIndex += increment
      columnIndex += 1

  def checkVisibility(self):
    for direction in all_directions:
      if direction == Direction.NORTH or direction == Direction.SOUTH:
        self.checkVisibilityVertically(direction)
      else:
        self.checkVisibilityHorizontally(direction)

  def overlayVisibilityMaps(self, map1, map2):
    map1Length = len(map1[0])
    map1Height = len(map1)
    map2Length = len(map2[0])
    map2Height = len(map2)
    if map1Length != map2Length or map1Height != map2Height:
      raise RuntimeError("Cannot overlay maps of differentSizes")

    newMap = self.createDefaultVisibilityMap(1)

    overlayMap = []
    i = 0
    while i < map1Length:
      j = 0
      while j < map1Height:
        newMap[j][i] = map1[j][i] * map2[j][i]
        j += 1
      i += 1

    return newMap

  def getVisibilityMap(self):
    totalMap = self.createDefaultVisibilityMap(1)
    for direction in all_directions:
      totalMap = self.overlayVisibilityMaps(totalMap, self.visibilityMap[direction])
    return totalMap

f = open("input.txt", "r")
forest = ForestMap(f.readlines())
vis_map = forest.getVisibilityMap()

max_score = 0


for line in vis_map:
  print(line)
  for num in line:
    if num > max_score:
      max_score = num

print(max_score)