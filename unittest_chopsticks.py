#!/usr/bin/env python

import unittest

from chopsticks import *


class TestChopsticks(unittest.TestCase):

  def setUp(self):
    self.game = ChopsticksGame()


  def testBasicGame(self):
    self.game.players[PLAYER_1].hands = [0,1]
    self.game.players[PLAYER_2].hands = [0,4]
    self.game.playerToMove = PLAYER_1
    self.game.doTurn('11')
    winningPlayer = self.game.checkForWinningPlayer()
    self.assertEqual(winningPlayer, PLAYER_1)


  def testValidateRolloverMove(self):
    self.game.players[PLAYER_1].hands = [4,0]
    self.game.players[PLAYER_2].hands = [4,0]
    self.game.playerToMove = PLAYER_1
    self.game.doTurn('00')
    winningPlayer = self.game.checkForWinningPlayer()
    self.assertEqual(winningPlayer, PLAYER_1)


  def testValidateInvalidMove(self):
    self.game.players[PLAYER_1].hands = [4,0]
    self.game.players[PLAYER_2].hands = [4,0]
    self.game.playerToMove = PLAYER_1
    validationResponse = self.game.checkIfMoveIsValid('bbq')
    self.assertEqual(INVALID_MOVE, validationResponse)


  def testValidateCannotSplit(self):
    self.game.players[PLAYER_1].hands = [4,2]
    self.game.playerToMove = PLAYER_1
    validationResponse = self.game.checkIfMoveIsValid('s')
    self.assertEqual(INVALID_CANNOT_SPLIT, validationResponse)


  def testValidateHittingWithEmptyHand(self):
    self.game.players[PLAYER_1].hands = [0,2]
    self.game.players[PLAYER_2].hands = [1,1]
    self.game.playerToMove = PLAYER_1
    validationResponse = self.game.checkIfMoveIsValid('00')
    self.assertEqual(INVALID_NO_FINGERS_BEING_USED, validationResponse)


  def testValidateHittingAnEmptyHand(self):
    self.game.players[PLAYER_1].hands = [1,1]
    self.game.players[PLAYER_2].hands = [0,1]
    self.game.playerToMove = PLAYER_1
    validationResponse = self.game.checkIfMoveIsValid('00')
    self.assertEqual(INVALID_NO_FINGERS_BEING_USED, validationResponse)


  def testSplit(self):
    self.game.players[PLAYER_1].hands = [4,0]
    self.game.players[PLAYER_2].hands = [1,1]
    self.game.playerToMove = PLAYER_1
    self.game.doTurn('s 22')
    self.assertEqual(self.game.players[PLAYER_1].hands, [2,2])

  def testSplit2(self):
    self.game.players[PLAYER_1].hands = [4,0]
    self.game.players[PLAYER_2].hands = [1,1]
    self.game.playerToMove = PLAYER_1
    self.game.doTurn('s 13')
    self.assertEqual(self.game.players[PLAYER_1].hands, [1,3])

  def testValidateHittingAnEmptyHand(self):
    self.game.players[PLAYER_1].hands = [4,0]
    self.game.players[PLAYER_2].hands = [1,1]
    self.game.playerToMove = PLAYER_1
    validationResponse = self.game.checkIfMoveIsValid('s 12')
    self.assertEqual(INVALID_CANNOT_SPLIT, validationResponse)



def suite():
  runSuite = unittest.TestSuite()
  for _name,_class in globals().items():
    if _name.startswith('Test'):
      runSuite.addTest(unittest.makeSuite(_class))
  return runSuite

if __name__ == '__main__':
  import sys
  if len(sys.argv) > 1:
    unittest.main()
  else:
    unittest.TextTestRunner().run(suite())
