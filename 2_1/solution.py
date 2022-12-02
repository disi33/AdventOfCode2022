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

class MoveTuple:
  def __init__(self, playerMove: Move, opponentMove: Move):
    self.playerMove = playerMove
    self.opponentMove = opponentMove

  def __hash__(self):
    hashableString = f"{self.playerMove},{self.opponentMove}"
    return hashableString.__hash__()

  def __eq__(self, comparee):
    return comparee.opponentMove == self.opponentMove and comparee.playerMove == self.playerMove


# [player move, opponent move]
resultMap = {
  MoveTuple(Move.ROCK, Move.ROCK): Result.DRAW,
  MoveTuple(Move.ROCK, Move.PAPER): Result.LOSS,
  MoveTuple(Move.ROCK, Move.SCISSORS): Result.WIN,
  MoveTuple(Move.SCISSORS, Move.ROCK): Result.LOSS,
  MoveTuple(Move.SCISSORS, Move.PAPER): Result.WIN,
  MoveTuple(Move.SCISSORS, Move.SCISSORS): Result.DRAW,
  MoveTuple(Move.PAPER, Move.ROCK): Result.WIN,
  MoveTuple(Move.PAPER, Move.PAPER): Result.DRAW,
  MoveTuple(Move.PAPER, Move.SCISSORS): Result.LOSS
}

class Round:
  def __init__(self, line: str):
    self.score = 0
    inputs = line.strip().split(sep=" ")
    self.opponentMove = self.parseOpponent(inputs[0])
    self.playerMove = self.parsePlayer(inputs[1])
    self.calculateScore()

  def parseOpponent(self, move):
    if move == "A":
      return Move.ROCK
    if move == "B":
      return Move.PAPER
    if move == "C":
      return Move.SCISSORS
    raise InputError(Player.OPPONENT, move)

  def parsePlayer(self, move):
    if move == "X":
      return Move.ROCK
    if move == "Y":
      return Move.PAPER
    if move == "Z":
      return Move.SCISSORS
    raise InputError(Player.PLAYER, move)

  def calculateScore(self):
    resultIndex = MoveTuple(self.playerMove, self.opponentMove)
    result = resultMap[resultIndex]
    self.score = self.playerMove.value + result.value
      
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