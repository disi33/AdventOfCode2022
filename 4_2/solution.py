#!/bin/python3

class Section:
  def __init__(self, line: str):
    strippedLine = line.strip()
    indexStrings = strippedLine.split('-')
    self.start = int(indexStrings[0])
    self.end = int(indexStrings[1])
  
  def fullyContains(self, otherSection):
    return otherSection.start >= self.start and otherSection.end <= self.end
  
  def partiallyContains(self, otherSection):
    return otherSection.start >= self.start and otherSection.start <= self.end \
           or otherSection.end >= self.start and otherSection.end <= self.end

class Comparison:
  def __init__(self, line3):
    strippedLine = line.strip()
    sectionStrings = strippedLine.split(',')
    self.section1 = Section(sectionStrings[0])
    self.section2 = Section(sectionStrings[1])

  def hasFullOverlap(self):
    return self.section1.fullyContains(self.section2) or self.section2.fullyContains(self.section1)

  def hasPartialOverlap(self):
    return self.section1.partiallyContains(self.section2) or self.section2.partiallyContains(self.section1)

f = open("input.txt", "r")
count = 0
for line in f:
    comparison = Comparison(line)
    if comparison.hasPartialOverlap():
      count += 1

print(count)