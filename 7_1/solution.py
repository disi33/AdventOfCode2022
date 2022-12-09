#!/bin/python3

from parser import Parser

class File:
  def __init__(self, name, size):
    self.name = name
    self.size = size
  
  def getSize(self):
    return self.size

class Directory:
  def __init__(self, name):
    self.files = []
    self.directories = {}
  
  def getSize(self):
    totalSize = 0
    for f in self.files:
      totalSize += f.getSize()
    for d in self.directories.keys():
      totalSize += self.directories[d].getSize()
    return totalSize

  def addFile(self, name, size):
    self.files.append(File(name, size))

  def addDirectory(self, name):
    self.directories[name] = Directory(name)

  def getDirectories(self):
    return list(self.directories.values())

class DirectoryTreeBuilder:
  def __init__(self):
    self.currentDirectory = None
    self.root = None
    self.directoryStack = []

  def changeDirectory(self, name):
    # move up in hierarchy
    if name == "..":
      self.currentDirectory = self.directoryStack.pop()
      return

    # create new folder if it doesnät exist and move to it
    newDirectory = Directory(name)
    if not self.root:
      self.root = Directory(name)
      self.currentDirectory = self.root
      self.directoryStack.append(self.currentDirectory)
    else:
      self.currentDirectory.addDirectory(name)
      self.directoryStack.append(self.currentDirectory)
      self.currentDirectory = self.currentDirectory.directories[name]

  def addFile(self, name, size):
    self.currentDirectory.addFile(name, int(size))

class TreeIterator:
  def __init__(self, treeBuilder):
    self.root = treeBuilder.root

  def getAllDirectories(self):
    directories = [self.root]
    directories = directories + self.getSubDirectories(self.root)
    return directories

  def getSubDirectories(self, directory):
    subDirectories = []
    dirs = directory.getDirectories()
    subDirectories = subDirectories + dirs
    for subDir in dirs:
      subDirectories = subDirectories + self.getSubDirectories(subDir)
    return subDirectories


tokenDefinitions = {
  "commandStart": "\$",
  "changeDirectory": "cd",
  "listDirectory": "ls",
  "directoryIdentifier": "dir",
  "number": "([0-9])+",
  "identifier": "[a-zA-Z.]([a-zA-Z0-9\._])+",
  "path": "(/?|\.\.|([a-zA-Z0-9\._])+)"
}

grammarRules = {
  "output": "(c=command)+",
  "command": "t:commandStart (cdCommand | lsCommand)",
  "cdCommand": "t:changeDirectory p=t:path <changeDirectory>",
  "lsCommand": "t:listDirectory lsOutputLine+",
  "lsOutputLine": "dirOutput | fileOutput",
  "dirOutput": "t:directoryIdentifier t:identifier",
  "fileOutput": "s=t:number f=t:identifier <addFile>"
}

treeBuilder = DirectoryTreeBuilder()

actions = {
  "changeDirectory": lambda context : treeBuilder.changeDirectory(context["p"]),
  "addFile": lambda context : treeBuilder.addFile(context["f"], context["s"]),
}

f = open("input.txt", "r")
parser = Parser(tokenDefinitions, grammarRules, actions, "output", f.readlines(), 1)
parser.parse()

iterator = TreeIterator(treeBuilder)
directories = iterator.getAllDirectories()
totalSize = 0
for d in directories:
  size = d.getSize()
  if size <= 100000:
    totalSize += size

print(totalSize)

