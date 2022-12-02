#!/bin/python3

import array

class Elf:
  def __init__(self, number):
    self.number = number
    self.calories = 0

  def addCalories(self, calories):
    newCalories = calories
    if isinstance(calories, str):
      newCalories = int(newCalories)
    self.calories += newCalories

  def getCalories(self):
    return self.calories

class Expedition:
  def __init__(self, maxCount):
    self.elfIndex = 0
    self.maxCount = maxCount
    self.elves = []

  def addNewElf(self):
    self.elfIndex += 1
    newElf = Elf(self.elfIndex)
    self.elves.append(newElf)
    return newElf

  def sortAsc(self, arr):
    return sorted(arr)


  def getHighestCalories(self):
    maxValues = array.array('i', [])
    for elf in self.elves:
      elfCalories = elf.getCalories()
      print(elfCalories)
      if len(maxValues) < self.maxCount:
        maxValues.append(elfCalories)
      else:
        index = 0
        while(index < len(maxValues)):
          if elfCalories > maxValues[index]:
            maxValues[index] = elfCalories
            index = len(maxValues) + 1
          else:
            index += 1
          maxValues = self.sortAsc(maxValues)

    print()
    
    total = 0
    for maxValue in maxValues:
      print(maxValue)
      total += maxValue

    print()
    
    return total

f = open("input.txt", "r")
expedition = Expedition(3)
currentElf = expedition.addNewElf()
for line in f:
  line = line.strip()
  if line == "":
    currentElf = expedition.addNewElf()
  else:
    currentElf.addCalories(line)

print(expedition.getHighestCalories())