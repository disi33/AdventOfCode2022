#!/bin/python3

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
  def __init__(self):
    self.elfIndex = 0
    self.elves = []

  def addNewElf(self):
    self.elfIndex += 1
    newElf = Elf(self.elfIndex)
    self.elves.append(newElf)
    return newElf

  def getHighestCalories(self):
    maxValue = 0
    for elf in self.elves:
      elfCalories = elf.getCalories()
      if elfCalories > maxValue:
        maxValue = elfCalories
    return maxValue

f = open("input.txt", "r")
expedition = Expedition()
currentElf = expedition.addNewElf()
for line in f:
  line = line.strip()
  if line == "":
    currentElf = expedition.addNewElf()
  else:
    currentElf.addCalories(line)

print(expedition.getHighestCalories())