import pygame
from engine.Engine import Level
from gui.Gui import Gui
from gui.Components import Button, Slider, Title, CheckBox, OrangeLabel
from event.EventHandler import IEventHandler, EventDispatcher
from event.Events import SliderEvent, CheckBoxEvent, ButtonClickEvent, LabelChange
from threading import Thread
from time import sleep
from misc.Constants import *

class MainMenu(Level):

	def __init__(self):
		Level.__init__(self, size=(200, 200))

	def update(self, time, events):
		pass

class GameLevel(Level):

	def __init__(self):
		Level.__init__(self, size=(860, 800))
		self.state = False
		self.time = 0

		self.game = GameSurface(self)

		self.gui = Gui(self, (260, 800), offset=(600, 0))

		test1 = Button((100, 25), self.gui, offset=(0, 0))
		test1.name = "bearing"
		self.gui.add_component(test1)

		test = Button((100, 25), self.gui, offset=(0, 30))
		self.gui.add_component(test)


		test = Button((100, 25), self.gui, offset=(0, 60))
		test.name = "exit"
		self.gui.add_component(test)

		test = Button((100, 25), self.gui, offset=(0, 90))
		self.gui.add_component(test)

		test = Slider(self.gui, offset=(25, 130))
		test.name = "velocity"
		self.gui.add_component(test)

		test = Slider(self.gui, offset=(25, 400))
		test.name = "notvelocity"
		self.gui.add_component(test)

		test = Title("Robot Settings", self.gui, 0, offset=(25, 500))
		test.name = "notvelocity"
		self.gui.add_component(test)

		test = CheckBox("Display Location Overlay", self.gui, offset=(25, 600))
		test.name = "displaylocation"
		self.gui.add_component(test)

		test = CheckBox("Display Paths", self.gui, offset=(25, 625))
		test.name = "displaypath"
		self.gui.add_component(test)

		test = OrangeLabel("Bearing (deg)", "0.0", self.gui, offset=(25, 700))
		test.name = "bearing"
		self.gui.add_component(test)

		self.thread = None

	def dopath(self):
		sleep(5)

	def update(self, time, events):

		if self.thread is None or not self.thread.isAlive():
			print("calculating path")
			self.thread = Thread(target=self.dopath)
			self.thread.start()

		self.time += time
		'''
		if self.time > 1:
			self.fill((0, 0, 0))
			self.time = 0
		elif self.time > 0.5:
			self.fill((255, 255, 255))
		'''
		#self.fill((255, 255, 255))
		self.gui.update(time, events)
		self.game.update(time, events)


class GameSurface(Level, IEventHandler):

	def __init__(self, parent):
		Level.__init__(self, size=(600, 800))
		IEventHandler.__init__(self)
		self.parent = parent
		self.mapimg = pygame.image.load("assets/img/map.png")
		self.rect = self.mapimg.get_rect()
		self.blit(self.mapimg, self.rect)

		self.test = pygame.Surface((50, 50))
		self.test.fill((0, 0, 0))
		self.testrect = self.test.get_rect()
		self.x, self.y = 50.0, 50.0
		self.velocity = [50, 50]
		self.direction = [1, 1]

		self.surfrect = pygame.Rect(0,0,0,0)
		self.rectlist = [pygame.Rect(100,100,100,100),pygame.Rect(100,100,100,100),pygame.Rect(100,100,100,100),pygame.Rect(100,100,100,100),pygame.Rect(100,100,100,100),pygame.Rect(100,100,100,100),pygame.Rect(100,100,100,100)]
		self.color = (0, 0, 0)

	def update(self, time, events):



		# this isnt very efficient at all but what the heck
		#self.blit(self.mapimg, self.mapimg.get_rect())
		self.blit(self.mapimg.subsurface(self.testrect.x, self.testrect.y, self.testrect.width, self.testrect.height), self.testrect)
		self.blit(self.mapimg.subsurface(self.surfrect), self.surfrect)


		self.x += time * self.velocity[0] * self.direction[0]
		self.y += time * self.velocity[1] * self.direction[1]

		EventDispatcher().send_event(LabelChange("bearing", "(" + str(int(self.x)) + ", " + str(int(self.y)) + ")"))

		self.testrect.x = self.x
		self.testrect.y = self.y

		if self.testrect.right > 555: self.direction[0] = -1
		if self.testrect.left < 5: self.direction[0] = 1
		if self.testrect.bottom > 795: self.direction[1] = -1
		if self.testrect.top < 5: self.direction[1] = 1

		font = pygame.font.Font(FONT_REGULAR, 12)
		surf = font.render("something above", True, (0, 0, 0))
		self.surfrect.width = surf.get_rect().width
		self.surfrect.height = surf.get_rect().height
		self.surfrect.x = self.testrect.center[0] - (surf.get_rect().width / 2)
		self.surfrect.y = self.testrect.y - 20

		self.blit(surf, self.surfrect)

		self.test.fill(self.color)
		self.blit(self.test, self.testrect)

		self.parent.blit(self, self.rect)

	def event_handler(self, event):
		#print event.name
		if event.istype(SliderEvent) and event.name is "velocity":
			self.velocity[0], self.velocity[1] = event.slidervalue, event.slidervalue
		if event.istype(CheckBoxEvent) and event.name is "displaypath":
			if event.checked:
				self.color = (255, 255, 255)
			else:
				self.color = (0, 0, 0)
		if event.istype(ButtonClickEvent) and event.name == "bearing":
			EventDispatcher().send_event(LabelChange("bearing", str(self.x)))