#!/bin/python3

class DataStream:
  def __init__(self, file):
    self.file = file
    self.nextCharacter = self.file.read(1)
    self.hasEnded = not self.nextCharacter

  def receiveCharacter(self):
    if not self.hasEnded:
      currentCharacter = self.nextCharacter
      self.nextCharacter = self.file.read(1)
      self.hasEnded = not self.nextCharacter
      return currentCharacter
    return None

class RollingBuffer:
  def __init__(self, size):
    self.size = size
    self.buffer = []
    self.counter = 0

  def add(self, item):
    self.buffer.append(item)
    if len(self.buffer) > self.size:
      del self.buffer[0]
    self.counter += 1

  def initialize(self, dataStream):
    i = 0
    while i < self.size:
      self.add(dataStream.receiveCharacter())
      i+=1

  def getBufferLength(self):
    return len(self.buffer)
  
  def areContentsAllDifferent(self):
    if len(self.buffer) < 2:
      return False
    index = 1
    while index < len(self.buffer):
      comparisonIndex = 0
      while comparisonIndex < index:
        if self.buffer[comparisonIndex] == self.buffer[index]:
          return False
        comparisonIndex += 1
      index += 1
    return True

f = open("input.txt", "r")
dataStream = DataStream(f)
bufferSize = 14
buffer = RollingBuffer(bufferSize)
buffer.initialize(dataStream)
while not buffer.areContentsAllDifferent() and not dataStream.hasEnded:
  buffer.add(dataStream.receiveCharacter())

if dataStream.hasEnded:
  print("Stream has ended")
else:
  print(buffer.counter)

