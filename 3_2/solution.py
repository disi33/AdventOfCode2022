#!/bin/python3

import array

class BackPack:
  def __init__(self, contents: str):
    strippedContents = contents.strip()
    self.contents = bytes(strippedContents, 'UTF-8')

  def findCommonItems(self, otherContents):
    commonItems = array.array('b', [])
    for character in self.contents:
      if character in otherContents:
        commonItems.append(character)
    return commonItems

class Group:
  def __init__(self, line1, line2, line3):
    self.backpack1 = BackPack(line1)
    self.backpack2 = BackPack(line2)
    self.backpack3 = BackPack(line3)
    self.badge = self.findBadge()

  def findBadge(self):
    intersect = self.backpack1.findCommonItems(self.backpack2.contents)
    return self.backpack3.findCommonItems(intersect)[0]

  def calculateScore(self):
    # transform lowercase characetrs to score
    itemByteValue = self.badge - 0x60
    if itemByteValue < 0:
      # if value is negative character was uppercase: adjust
      itemByteValue += 0x3A
    return itemByteValue

f = open("input.txt", "r")
totalScore = 0
index = 0
linebuffer = ['', '']
for line in f:
  if index < 2:
    linebuffer[index] = line
  else:
    group = Group(linebuffer[0], linebuffer[1], line)
    score = group.calculateScore()
    totalScore += score
  index = 0 if index == 2 else index+1

print(totalScore)