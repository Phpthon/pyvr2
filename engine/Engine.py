import pygame
import sys
from event.EventHandler import *
from event.Events import ButtonClickEvent, LevelChangeEvent
from misc.Constants import *
from map.Levels import GameLevel, MainMenu, PauseMenu

class GameEngine(IEventHandler, object):

	def __init__(self):
		IEventHandler.__init__(self)
		pygame.init()
		self.display = None
		self.level = None
		self.changinglevels = False
		self.fps = 120
		self.clock = pygame.time.Clock()
		self.ticktime = self.clock.tick(self.fps)

		self.paused = False

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

			if self.paused:
				if not self.pause_menu.init:
					self.pause_menu.set_alpha(35)
					print("done")
					#self.pause_menu.blit(self.display, (0, 0))
					#self.pause_menu.gui.redraw_initial()
					self.pause_menu.init = True
				self.display.blit(self.pause_menu, (0, 0))
				self.pause_menu.update(ticktimeseconds, events)
				
			else:
				self.level.update(ticktimeseconds, events)
				self.display.blit(self.level, self.level.get_rect())

			pygame.display.flip()

	def change_level(self, level):
		self.display = pygame.display.set_mode((level.get_rect().width, level.get_rect().height))
		self.pause_menu = PauseMenu(self.display)
		#self.pause_menu.rect.x = (self.level.rect.width - self.pause_menu.rect.width) / 2
		#self.pause_menu.rect.y = (self.level.rect.height - self.pause_menu.rect.height) / 2
		self.level = level

	def event_handler(self, event):
		if event.istype(ButtonClickEvent) and event.name is "exit":
			pygame.event.post(pygame.event.Event(pygame.QUIT))
		if event.istype(ButtonClickEvent) and event.name is "pause":
			self.paused = True
		if event.istype(ButtonClickEvent) and event.name is "resume":
			self.paused = False
			self.pause_menu.init = False
		if event.istype(LevelChangeEvent) and event.level is LEVEL_MAIN_MENU:
			self.change_level(MainMenu())
		if event.istype(LevelChangeEvent) and event.level is LEVEL_GAME:
			self.change_level(GameLevel())

