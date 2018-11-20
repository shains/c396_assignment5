#!/usr/bin/env python3

import numpy as np

PLAYER_1 = 'p1'
PLAYER_2 = 'p2'
SPLIT = 's'
POSSIBLE_MOVES = ['01','00','10','11',SPLIT]
HELP_TEXT = """
Moving examples- 
  Using my 0 index hand, hit other player's 1 index hand: 01
  Using my 1 index hand, hit other player's 1 index hand: 11
  Split: s
"""

INVALID_MOVE                  = 'Invalid move, possible moves are: ' + str(POSSIBLE_MOVES)
INVALID_CANNOT_SPLIT          = 'Bad move. Cannot split.'
INVALID_NO_FINGERS_BEING_USED = 'Bad move.  Hand must have some fingers to be used'

# isomorphisms, taken from https://en.wikipedia.org/wiki/Chopsticks_(hand_game), however includes with adding to self
isomorphs = np.array(( (2,1,1,1),
                       #(?,?,0,0), discuss as group
                       (2,1,4,1),
                       (2,1,2,0),
                       (3,1,1,1),
                       (3,2,1,1),
                       (3,2,4,1),
                       (3,3,3,0),
                       (3,1,1,0),
                       (3,2,1,0),
                       (3,3,1,0),
                       (1,0,1,0),
                       (2,0,1,0),
                       (3,0,1,0),
                       (2,1,1,0),
                       (4,2,1,0),
                       (4,4,1,0),
                       (1,1,1,0)
                       ))

class Player:
  def __init__(self):
    self.hands = [1,1]

  def canSplit(self):
    return self.aHandIsEven() and self.aHandIsEmpty()

  def aHandIsEven(self):
    return (self.hands[0] % 2 == 0 and self.hands[0] != 0) \
        or (self.hands[1] % 2 == 0 and self.hands[1] != 0)

  def aHandIsEmpty(self):
    return self.hands[0] == 0 or self.hands[1] == 0


class ChopsticksGame:

  def __init__(self):
    self.players = {PLAYER_1 : Player(), PLAYER_2 : Player()}
    self.playerToMove = PLAYER_1
    self.gameStateHistory = []

  def printGameState(self):
    print('p1:' + str(self.players[PLAYER_1].hands) + '  p2:' + str(self.players[PLAYER_2].hands) + '  Player to move: ' + self.playerToMove)


  def opponent(self, player):
    if player == PLAYER_1:
      return PLAYER_2
    return PLAYER_1

  def checkIfMoveIsValid(self, move):
    if move not in POSSIBLE_MOVES:
      return INVALID_MOVE
    player = self.players[self.playerToMove]
    opponentPlayer = self.players[self.opponent(self.playerToMove)]
    if move == SPLIT and not player.canSplit() :
      return INVALID_CANNOT_SPLIT
    if move != SPLIT: 
      playerHand = int(move[0])
      opponentHand = int(move[1])
      if player.hands[playerHand] == 0 or opponentPlayer.hands[opponentHand] == 0:
        return INVALID_NO_FINGERS_BEING_USED

  def inputMove(self):
    #Swap this function out with AI or use it to build tree - but be sure to use validation 
    while True:
      move = input('(' + self.playerToMove + ') : ')
      print(str(move))
      validationString = self.checkIfMoveIsValid(move)
      if validationString:
        #Error with move, print error and ask for move again
        print(validationString)
        continue
      else:
        break
    return move


  def doMove(self, move):
    if move == SPLIT:
      fromHandIndex = 0 if self.players[self.playerToMove].hands[1] == 0 else 1
      splitAmount = int(self.players[self.playerToMove].hands[fromHandIndex] / 2)
      self.players[self.playerToMove].hands[0] = splitAmount
      self.players[self.playerToMove].hands[1] = splitAmount
    else:
      playerHand = int(move[0])
      opponentHand = int(move[1])
      self.players[self.opponent(self.playerToMove)].hands[opponentHand] += self.players[self.playerToMove].hands[playerHand]
      if self.players[self.opponent(self.playerToMove)].hands[opponentHand] == 5:
        self.players[self.opponent(self.playerToMove)].hands[opponentHand] = 0

  def switchPlayerToMove(self):
    self.playerToMove = self.opponent(self.playerToMove)

  def situationalSuperKoViolated(self):
    return self.gameState() in self.gameStateHistory

  def checkForWinningPlayer(self):
    if self.situationalSuperKoViolated():
      return self.playerToMove
    #TODO: Doesn't work, write unit tests for this
    if not self.playerHasValidMove():
      return self.opponent(self.playerToMove)
    for player in [PLAYER_1, PLAYER_2]:
      hands = self.players[player].hands
      if hands[0] == 0 and hands[1] == 0:
        return self.opponent(player)

  def gameState(self):
    return [''.join([str(self.players[PLAYER_1].hands), str(self.players[PLAYER_2].hands), self.playerToMove])]

  def playerHasValidMove(self):
    for move in POSSIBLE_MOVES:
      if self.checkIfMoveIsValid(move):
        return True
    return False


  def saveGameStateHistory(self):
    self.gameStateHistory += self.gameState()
    #print(self.gameStateHistory)

  def doTurn(self, move):
    # Returns the winning player if the game has ended
    self.saveGameStateHistory()
    self.doMove(move)
    self.switchPlayerToMove()

    winningPlayer = self.checkForWinningPlayer()
    if winningPlayer:
      print('Winning player: ' + winningPlayer)
      return winningPlayer
    return False


  def play(self):
    print(HELP_TEXT)
    while True:
      self.printGameState()
      move = self.inputMove()
      winResult = self.doTurn(move)
      if winResult:
        break

  


if __name__ == '__main__':
  ChopsticksGame().play()
