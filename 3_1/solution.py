#!/bin/python3

class BackPack:
  def __init__(self, contents: str):
    strippedContents = contents.strip()
    contentLength = len(strippedContents)
    if contentLength % 2 != 0:
      raise TypeError("backpack contents must be divisible")
    halfwayPoint = int(contentLength/2)
    self.compartment1 = bytes(strippedContents[:halfwayPoint], 'UTF-8')
    self.compartment2 = bytes(strippedContents[-halfwayPoint:], 'UTF-8')
    self.commonItem = self.findCommonItem()

  def findCommonItem(self):
    for character in self.compartment1:
      if character in self.compartment2:
        return character

  def calculateScore(self):
    # transform lowercase characetrs to score
    itemByteValue = self.commonItem - 0x60
    if itemByteValue < 0:
      # if value is negative character was uppercase: adjust
      itemByteValue += 0x3A
    return itemByteValue

f = open("input.txt", "r")
totalScore = 0
for line in f:
  backpack = BackPack(line)
  score = backpack.calculateScore()
  print(f"{line}: {score}")
  totalScore += score

print(totalScore)