#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In the example, we draw randomly 1000 red points 
on the window.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QBasicTimer, QTimer
import sys, random
from enum import Enum
import math
import csv
import csv

class Direction(Enum):
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4

class Example(QWidget):
	
	BoardWidth = 0
	BoardHeight = 0
	x_max = 0
	y_max = 0
	snake = []
	direction = 1
	game_started = False
	speed = 0
	
	#Apple settings
	apple_pos = [0, 0]
	apple_color = 0
	apple_number = 0
	apple_active = False
	apple_eaten = False
	
	def __init__(self):
		super().__init__()
		
		self.initUI()
		
		
	def initUI(self):      
		#Initialize board
		self.BoardWidth = 2000
		self.BoardHeight = 2000
		self.setGeometry(0, 0, self.BoardWidth, self.BoardHeight)
		self.setWindowTitle('Snake')
		#Set background
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)
		
		#set the maze
		self.maze = self.loadmaze('pos_maze.csv')
		
		#Set snake parameters
		self.direction = 4
		self.x_max = 125
		self.y_max = 125
		self.snake =[[(self.x_max // 2 - 1), self.y_max // 2], [(self.x_max // 2), self.y_max // 2], [(self.x_max // 2 + 1), self.y_max // 2], [(self.x_max // 2 + 2), self.y_max // 2] , [(self.x_max // 2 + 3), self.y_max // 2]]
		self.speed = 50
		#Has the game begun?
		game_started = False
		
		#Set timer
		self.timer = QBasicTimer()
		self.timer.start(self.speed, self)
		
		#Apple settings
		margin = 20
		self.apple_pos[0] = random.randint(margin, self.x_max - margin)
		self.apple_pos[1] = random.randint(margin, self.y_max - margin)
		self.apple_color = Qt.blue
		
		random.seed()
		self.show()
		
		
	def loadmaze(self, filename):
		s = set()
		with open(filename) as f:
			reader = csv.reader(f)
			for row in reader:
				s.add(int(row[0]))
		return s	

	def paintEvent(self, e):
	
		qp = QPainter()
		qp.begin(self)
		self.drawSnake(qp)
		self.drawApple(qp)
		for i in self.maze:
			r = i //self.y_max
			c = i % self.y_max
			qp.drawRect(r * self.BoardWidth // self.x_max, c * self.BoardHeight // self.y_max, self.BoardWidth // self.x_max, self.BoardHeight // self.y_max)
		qp.end()
		self.update()
		
	def drawSnake(self, qp):
		qp.setBrush(Qt.red)
		qp.setPen(Qt.yellow)
		size = self.size()
		for i in self.snake:
			qp.drawRect((i[0] * self.BoardWidth // self.x_max), (i[1] * self.BoardHeight // self.y_max), self.BoardWidth // self.x_max, self.BoardHeight // self.y_max)
		self.update()

	def drawApple(self, qp):
		qp.setBrush(Qt.blue)
		qp.setPen(Qt.green)
		radx = 10
		rady = 20
		qp.drawEllipse((self.apple_pos[0] * self.BoardWidth // self.x_max), (self.apple_pos[1] * self.BoardHeight // self.y_max), radx, rady)
		self.update()

	def hitsWall(self, x, y):
		return (x == 0 or x == self.x_max or y == 0 or y == self.y_max)

	def calculatesCost(self, goal, state):
		return (math.pow(goal[0] - state[0], 2) + math.pow(goal[1] - state[1], 2))

	def keyPressEvent(self, e):
		self.game_started = True

	def next_state(self):
		current_x = self.snake[-1][0]
		current_y = self.snake[-1][1]
		#Determine next state:
		
		#Possible states: go up, down, right left
		#These contain the next state, the actions: 1-up, 2-down, 3-right, 4-left, and an unitialized cost
		next_possible_states = [ [current_x, current_y - 1], [current_x, current_y + 1], [current_x - 1, current_y], [current_x + 1, current_y] ]
		next_state = []
		cost = math.inf
		for i in next_possible_states:
			#Checks if next state is a valid one.
			maze_pos = self.y_max * i[0] + i[1]
			if maze_pos in self.maze:
				continue
			#If it is valid:
			if not self.hitsWall(i[0], i[1]) and i not in self.snake:
				aux = self.calculatesCost(self.apple_pos, i)
				if aux < cost:
					cost = aux
					next_state = i
		#If the successors state is the goal, the game will end (for now)
		if self.apple_pos == next_state:
			print("The apple was eaten!")
			sys.exit()
		if len(next_state) == 0:
			print("Game over! There were no more possible states")
			sys.exit()
		self.snake.append(next_state) 
		self.snake.pop(0)

	def timerEvent(self, e):
		if e.timerId() == self.timer.timerId():
			self.next_state()
		else:
			super(Example, self).timerEvent(e)

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
