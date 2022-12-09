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
      self.visibilityMap[direction] = self.createDefaultVisibilityMap()

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
      currentRowMaximum = -1
      searchIndex = startIndex
      while searchIndex != endIndex:
        currentHeight = self.forestGrid[rowIndex][searchIndex]
        if currentHeight > currentRowMaximum:
          currentRowMaximum = currentHeight
        else:
          self.visibilityMap[direction][rowIndex][searchIndex] = 0
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
      currentColumnMaximum = -1
      searchIndex = startIndex
      while searchIndex != endIndex:
        currentHeight = self.forestGrid[searchIndex][columnIndex]
        if currentHeight > currentColumnMaximum:
          currentColumnMaximum = currentHeight
        else:
          self.visibilityMap[direction][searchIndex][columnIndex] = 0
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

    newMap = self.createDefaultVisibilityMap(0)

    overlayMap = []
    i = 0
    while i < map1Length:
      j = 0
      while j < map1Height:
        newMap[j][i] = 1 if map1[j][i] == 1 or map2[j][i] == 1 else 0
        j += 1
      i += 1

    return newMap

  def getVisibilityMap(self):
    totalMap = self.createDefaultVisibilityMap(0)
    for direction in all_directions:
      totalMap = self.overlayVisibilityMaps(totalMap, self.visibilityMap[direction])
    return totalMap

f = open("input.txt", "r")
forest = ForestMap(f.readlines())
vis_map = forest.getVisibilityMap()

count = 0
for line in vis_map:
  for num in line:
    count += num

print(count)