#!/bin/python3

class TextMatrix:
  def __init__(self, lines):
    self.textmatrix = []
    lineCount = len(lines)
    columnCount = len(lines[len(lines)-1])
    self.lineCount = lineCount
    self.columnCount = columnCount
    lineIndex = 0
    columnIndex = 0
    while lineIndex < lineCount:
      self.textmatrix.append([])
      while columnIndex < columnCount:
        char = lines[lineIndex][columnIndex]
        self.textmatrix[lineIndex].append(char)
        columnIndex += 1
      columnIndex = 0
      lineIndex += 1

  def inverseMatrix(self):
    newLineCount = self.columnCount
    newColumnCount = self.lineCount
    newTextMatrix = []

    lineIndex = 0
    while lineIndex < newLineCount:
      newTextMatrix.append([])
      columnIndex = 0
      while columnIndex < newColumnCount:
        newTextMatrix[lineIndex].append(self.getContentAt((newColumnCount-columnIndex-1), lineIndex))
        columnIndex += 1
      lineIndex += 1

    self.lineCount = newLineCount
    self.columnCount = newColumnCount
    self.textmatrix = newTextMatrix

  def getContentAt(self, lineIndex, columnIndex):
    return self.textmatrix[lineIndex][columnIndex]

  def printMatrix(self):
    self.printMatrixInternal(self.textmatrix)

  def printMatrixInternal(self, matrix):
    for line in matrix:
      for char in line:
        print(char, end="")
      print("")

  def removeLine(self, lineIndex):
    lineToRemove = self.textmatrix[lineIndex]
    self.textmatrix.remove(lineToRemove)
    self.lineCount -= 1

  def removeColumn(self, columnIndex):
    for line in self.textmatrix:
      del line[columnIndex]
    self.columnCount -= 1

  def getLine(self, lineIndex):
    return self.textmatrix[lineIndex]

  def getColumn(self, columnIndex):
    column=[]
    for line in self.textmatrix:
      column.append(line[columnIndex])
    return column

class Crate:
  def __init__(self, content: str):
    self.content = content
  
  def getContent(self):
    return self.content

class Dock:
  def __init__(self, lines):
    self.columns = []
    self.populateWithInput(lines)

  def populateWithInput(self, lines):
    input = TextMatrix(lines)
    input.inverseMatrix()
    input.removeColumn(0)
    lineIndex = 0
    while True:
      firstChar = input.getContentAt(lineIndex, 0)
      if not (firstChar == " " or firstChar == "[" or firstChar == "]"):
        lineIndex += 1
      else:
        input.removeLine(lineIndex)
      if lineIndex >= input.lineCount:
        break
    
    lineIndex = 0
    while lineIndex < input.lineCount:
      self.addColumn(input.getLine(lineIndex))
      lineIndex += 1

  def addColumn(self, items):
    newColumn = []
    for item in items:
      if item.strip() != "":
        newColumn.append(Crate(item))
    self.columns.append(newColumn)

  def getColumn(self, index):
    return self.columns[index]

  def getTopMostContents(self):
    resultString = ""
    for column in self.columns:
      resultString += column[len(column)-1].getContent()
    return resultString
  
  def moveCrate(self, fromColumnIndex, toColumnIndex):
    fromColumn = self.getColumn(fromColumnIndex)
    toColumn = self.getColumn(toColumnIndex)
    crateToMove = fromColumn.pop(len(fromColumn)-1)
    toColumn.append(crateToMove)

class Instruction:
  def __init__(self ,text):
    self.repetitions = int(text.split("move ")[1].split(" from ")[0])
    self.fromColumnIndex = int(text.split("from ")[1].split(" to ")[0])-1
    self.toColumnIndex = int(text.split("to ")[1])-1

class Orchestrator:
  def __init__(self, dock, instructions):
    self.dock = dock
    self.instructions = instructions

  def run(self):
    for instruction in self.instructions:
      i = 0
      while i < instruction.repetitions:
        i += 1
        self.dock.moveCrate(instruction.fromColumnIndex, instruction.toColumnIndex)

f = open("input.txt", "r")
crateLines = []
line = f.readline()
while not line.strip() == "":
  crateLines.append(line.replace("\n", ""))
  line = f.readline()

instructions = []
for line in f:
  instructions.append(Instruction(line.strip()))

dock = Dock(crateLines)
orchestrator = Orchestrator(dock, instructions)
orchestrator.run()
print(dock.getTopMostContents())

