#!/bin/python3

from enum import Enum

class Player(Enum):
  PLAYER = 1
  OPPONENT = 2

class Result(Enum):
  LOSS = 0
  DRAW = 3
  WIN = 6

class InputError(TypeError):
  def __init__(self,player,input):
    super().__init__(f"Invalid input for player '{player}': {input}")

class Move(Enum):
  ROCK = 1
  PAPER = 2
  SCISSORS = 3

class RoundRecord:
  def __init__(self, roundResult: Result, opponentMove: Move):
    self.roundResult = roundResult
    self.opponentMove = opponentMove

  def __hash__(self):
    hashableString = f"{self.roundResult},{self.opponentMove}"
    return hashableString.__hash__()

  def __eq__(self, comparee):
    return comparee.opponentMove == self.opponentMove and comparee.roundResult == self.roundResult


# [round result, opponent move]
resultMap = {
  RoundRecord(Result.WIN, Move.ROCK): Move.PAPER,
  RoundRecord(Result.WIN, Move.PAPER): Move.SCISSORS,
  RoundRecord(Result.WIN, Move.SCISSORS): Move.ROCK,
  RoundRecord(Result.DRAW, Move.ROCK): Move.ROCK,
  RoundRecord(Result.DRAW, Move.PAPER): Move.PAPER,
  RoundRecord(Result.DRAW, Move.SCISSORS): Move.SCISSORS,
  RoundRecord(Result.LOSS, Move.ROCK): Move.SCISSORS,
  RoundRecord(Result.LOSS, Move.PAPER): Move.ROCK,
  RoundRecord(Result.LOSS, Move.SCISSORS): Move.PAPER
}

class Round:
  def __init__(self, line: str):
    self.score = 0
    inputs = line.strip().split(sep=" ")
    self.opponentMove = self.parseOpponent(inputs[0])
    self.roundResult = self.parseResult(inputs[1])
    self.calculateScore()

  def parseOpponent(self, move):
    if move == "A":
      return Move.ROCK
    if move == "B":
      return Move.PAPER
    if move == "C":
      return Move.SCISSORS
    raise InputError(Player.OPPONENT, move)

  def parseResult(self, move):
    if move == "X":
      return Result.LOSS
    if move == "Y":
      return Result.DRAW
    if move == "Z":
      return Result.WIN
    raise InputError("Result", move)

  def calculateScore(self):
    resultIndex = RoundRecord(self.roundResult, self.opponentMove)
    playerMove = resultMap[resultIndex]
    self.score = playerMove.value + self.roundResult.value
      
  def getScore(self):
    return self.score

class Tournament:
  def __init__(self):
    self.rounds = []

  def addNewRound(self, line):
    newRound = Round(line)
    self.rounds.append(newRound)

  def calculateScore(self):
    totalScore = 0
    for round in self.rounds:
      totalScore += round.getScore()
    return totalScore

f = open("input.txt", "r")
tournament = Tournament()
for line in f:
  tournament.addNewRound(line)

print(tournament.calculateScore())