#!/usr/bin/env python3

# import numpy as np

PLAYER_1 = 'p1'
PLAYER_2 = 'p2'
SPLIT = 's'
POSSIBLE_MOVES = ['01', '00', '10', '11', SPLIT]
HELP_TEXT = """
Moving examples- 
  Using my 0 index hand, hit other player's 1 index hand: 
    01
  Using my 1 index hand, hit other player's 1 index hand: 
    11
  Split my 40 hand into 1 3:
    s 13
"""

INVALID_MOVE = 'Invalid move, possible moves are: ' + str(POSSIBLE_MOVES)
INVALID_CANNOT_SPLIT = 'Bad move. Cannot split.'
INVALID_NO_FINGERS_BEING_USED = 'Bad move.  Hand must have some fingers to be used'


class Player:
    def __init__(self):
        self.hands = [1, 1]

    def canSplit(self, endSplitState):
        """
    emptyHandIndex = None
    nonEmptyHandIndex = None
    if self.hands[0] == 0:
      emptyHandIndex = 0
      nonEmptyHandIndex = 1
    if self.hands[1] == 0:
      emptyHandIndex = 1
      nonEmptyHandIndex = 0
    if self.hands[nonEmptyHandIndex] <= 1:
      return False
    """
        if self.hands[0] == int(endSplitState[1]) and self.hands[1] == int(endSplitState[0]):
            return False
        # if int(endSplitState[0]) + int(endSplitState[1]) != self.hands[nonEmptyHandIndex]:
        # return False
        return True

    def isValidSplitMove(self, move):
        nonEmptyHand = self.hands[1] if self.hands[0] == 0 else self.hands[0]


class ChopsticksGame:

    def __init__(self):
        self.players = {PLAYER_1: Player(), PLAYER_2: Player()}
        self.playerToMove = PLAYER_1
        self.gameStateHistory = []

    def printGameState(self):
        print('p1:' + str(self.players[PLAYER_1].hands) + '  p2:' + str(
            self.players[PLAYER_2].hands) + '  Player to move: ' + self.playerToMove)

    def opponent(self, player):
        if player == PLAYER_1:
            return PLAYER_2
        return PLAYER_1

    def checkIfMoveIsValid(self, move):
        main_move = move.split(' ')[0]
        if main_move not in POSSIBLE_MOVES:
            return INVALID_MOVE
        player = self.players[self.playerToMove]
        opponentPlayer = self.players[self.opponent(self.playerToMove)]
        # Split moves
        if main_move == SPLIT:
            try:
                endSplitState = move.split(' ')[1]
                if not player.canSplit(endSplitState):
                    return INVALID_CANNOT_SPLIT
            except:
                return INVALID_CANNOT_SPLIT
            return ''

        # Regular moves
        playerHand = int(main_move[0])
        opponentHand = int(main_move[1])
        if player.hands[playerHand] == 0 or opponentPlayer.hands[opponentHand] == 0:
            return INVALID_NO_FINGERS_BEING_USED
        return ''

    def inputMove(self):
        # Swap this function out with AI or use it to build tree - but be sure to use validation

        Solver()
        """
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
		"""

    def Solver(self, depth):

        # Implementation of minimax tree

        result = -1
        if self.players[self.playerToMove].hands == [0, 0]:  # checks if winning state
            return result
        #print("check3")
        tempPlayers = {PLAYER_1: self.players[PLAYER_1], PLAYER_2: self.players[PLAYER_2]}
        tempPlayerToMove = self.playerToMove
        tempGameStateHistory = self.gameStateHistory
        for move in POSSIBLE_MOVES:
            # if move == SPLIT:
            # for i in range (1,4):
            #print("MOVE", move)
            print("Depth of node: ",depth)
            if self.checkIfMoveIsValid(move) == '':  # move is valid
                #print("MOVE2", move)

                self.playerToMove = tempPlayerToMove
                self.gameStateHistory = tempGameStateHistory
                self.players[PLAYER_1] = tempPlayers[PLAYER_1]
                self.players[PLAYER_2] = tempPlayers[PLAYER_2]

                self.saveGameStateHistory()
                self.printGameState()
                self.doMove(move)
                self.switchPlayerToMove()
                result = -self.Solver(depth + 1)
                if result == 1:
                    break
        return result

    def doMove(self, move):
        main_move = move.split(' ')[0]
        if main_move == SPLIT:
            endSplitState = move.split(' ')[1]
            fromHandIndex = 0 if self.players[self.playerToMove].hands[1] == 0 else 1
            self.players[self.playerToMove].hands[0] = int(endSplitState[0])
            self.players[self.playerToMove].hands[1] = int(endSplitState[1])
        else:
            playerHand = int(main_move[0])
            opponentHand = int(main_move[1])
            self.players[self.opponent(self.playerToMove)].hands[opponentHand] += self.players[self.playerToMove].hands[
                playerHand]
            if self.players[self.opponent(self.playerToMove)].hands[opponentHand] >= 5:
                self.players[self.opponent(self.playerToMove)].hands[opponentHand] = 0

    def switchPlayerToMove(self):
        self.playerToMove = self.opponent(self.playerToMove)

    def situationalSuperKoViolated(self):
        return self.gameState() in self.gameStateHistory

    def checkForWinningPlayer(self):
        if self.situationalSuperKoViolated():
            return self.playerToMove
        # TODO: Doesn't work, write unit tests for this
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
            if not self.checkIfMoveIsValid(move):
                return True
        return False

    def saveGameStateHistory(self):
        self.gameStateHistory += self.gameState()
        # print(self.gameStateHistory)

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
        print(self.Solver(1))

    """
  while True:
    self.printGameState()
    move = self.inputMove()
    winResult = self.doTurn(move)
    if winResult:
      break
  """


if __name__ == '__main__':
    ChopsticksGame().play()

