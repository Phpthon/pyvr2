import pygame
import sys
from event.EventHandler import *
from event.Events import ButtonClickEvent

class GameEngine(IEventHandler, object):

	def __init__(self):
		IEventHandler.__init__(self)
		pygame.init()
		self.display = None
		self.level = None
		self.changinglevels = False
		self.fps = 60
		self.clock = pygame.time.Clock()
		self.ticktime = self.clock.tick(self.fps)

	def init(self):
		pass

	def mainloop(self):
		while 1:
			self.ticktime = self.clock.tick(self.fps)
			ticktimeseconds = self.ticktime / 1000.0
			events = pygame.event.get()

			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.level.update(ticktimeseconds, events)
			self.display.blit(self.level, self.level.get_rect())

			pygame.display.flip()

	def change_level(self, level):
		self.display = pygame.display.set_mode((level.get_rect().width, level.get_rect().height))
		self.level = level

	def event_handler(self, event):
		if event.istype(ButtonClickEvent) and event.name is "exit":
			print("EXIT REQUEST: " + event.text)
			pass


class Level(pygame.Surface):
	
	def __init__(self, size=(500,500)):
		pygame.Surface.__init__(self, size)

	def update(self, time, events):
		pass