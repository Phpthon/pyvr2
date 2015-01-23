import pygame
from gui.Gui import Gui
from gui.Components import *
from event.EventHandler import IEventHandler, EventDispatcher
from event.Events import SliderEvent, CheckBoxEvent, ButtonClickEvent, LabelChange, LevelChangeEvent
from threading import Thread
from time import sleep
from misc.Constants import *
from misc.Entity import *
import random

class Level(pygame.Surface):
	
	def __init__(self, size=(500,500)):
		pygame.Surface.__init__(self, size)

	def update(self, time, events):
		raise NotImplementedError

class MainMenu(Level, IEventHandler):

	def __init__(self):
		Level.__init__(self, size=(500, 500))
		IEventHandler.__init__(self)

		self.gui = Gui(self, (500, 500), offset=(0, 0))

		test1 = PlayTitle("Python Virtual Robot", self.gui, offset=(self.gui.rect.center[0]-105, 50))
		test1.name = "test"
		self.gui.add_component(test1)

		test1 = Button("Start", 2, self.gui, offset=(self.gui.rect.center[0]-50, 130))
		test1.name = "start"
		self.gui.add_component(test1)

		test1 = Button("Exit", 0, self.gui, offset=(self.gui.rect.center[0]-50, 190))
		test1.name = "exit"
		self.gui.add_component(test1)

		#test1 = FlashingLabel("Testing", self.gui, offset=(self.gui.rect.center[0]-50, 200))
		#test1.name = "test"
		#self.gui.add_component(test1)

	def update(self, time, events):
		self.gui.update(time, events)

	def event_handler(self, event):
		if event.istype(ButtonClickEvent) and event.name is "start":
			EventDispatcher().send_event(LevelChangeEvent("test", LEVEL_GAME))

class GameLevel(Level):

	def __init__(self):
		Level.__init__(self, size=(860, 800))
		self.state = False
		self.time = 0

		self.game = GameSurface(self)

		self.gui = Gui(self, (260, 800), offset=(600, 0))

		test = MainTitle(self.gui, offset=(0, 0))
		self.gui.add_component(test)

		test = OrangeLabel("", "0.0", self.gui, offset=(155, 20), size=(70, 16))
		test.name = "current_time"
		self.gui.add_component(test)

		test = Title("Robot 1 : User Controlled", self.gui, 0, offset=(25, 100))
		self.gui.add_component(test)

		test = Slider("Velocity", self.gui, offset=(25, 145), increment=10.0, minvalue=150.0, maxvalue=300.0)
		test.name = "velocity"
		self.gui.add_component(test)

		test = Slider("Bearing", self.gui, offset=(25, 190), increment=10.0, minvalue=0.0, maxvalue=360.0)
		test.name = "bearing"
		self.gui.add_component(test)

		test = OrangeLabel("Position (x, y)", "0.0", self.gui, offset=(25, 240))
		test.name = "position"
		self.gui.add_component(test)

		test = OrangeLabel("Bearing (degrees)", "0.0", self.gui, offset=(25, 260))
		test.name = "bearing"
		self.gui.add_component(test)

		test = OrangeLabel("Score", "0.0", self.gui, offset=(25, 280))
		test.name = "score"
		self.gui.add_component(test)

		test = OrangeLabel("", "N/A", self.gui, offset=(25, 300))
		test.name = "location"
		self.gui.add_component(test)

		test = Title("Robot 2 : Automated", self.gui, 0, offset=(25, 310))
		self.gui.add_component(test)

		test = Slider("Velocity", self.gui, offset=(25, 355), increment=10.0, minvalue=150.0, maxvalue=300.0)
		test.name = "velocityai"
		self.gui.add_component(test)

		test = OrangeLabel("Position (x, y)", "0.0", self.gui, offset=(25, 405))
		test.name = "positionai"
		self.gui.add_component(test)

		test = OrangeLabel("Bearing (degrees)", "0.0", self.gui, offset=(25, 425))
		test.name = "bearingai"
		self.gui.add_component(test)

		test = OrangeLabel("Score", "0.0", self.gui, offset=(25, 445))
		test.name = "scoreai"
		self.gui.add_component(test)

		test = OrangeLabel("", "N/A", self.gui, offset=(25, 465))
		test.name = "locationai"
		self.gui.add_component(test)

		test = Title("General Settings", self.gui, 2, offset=(25, 475))
		self.gui.add_component(test)

		#test1 = FlashingLabel("Pulsating Label", self.gui, offset=(25, 300))
		#test1.name = "test"
		#self.gui.add_component(test1)

		test1 = TrafficLight(self.gui, offset=(180, 530))
		test1.name = "light"
		self.gui.add_component(test1)

		test1 = Button("Pause", 3, self.gui, offset=(60, 530))
		test1.name = "pause"
		self.gui.add_component(test1)

		test = Button("Menu", 1, self.gui, offset=(60, 560))
		test.name = "menu"
		self.gui.add_component(test)

		test = CheckBox("Display Treasures", self.gui, offset=(25, 675))
		test.name = "displaytreasure"
		self.gui.add_component(test)

		test = CheckBox("Display Paths", self.gui, offset=(25, 700))
		test.name = "displaypath"
		self.gui.add_component(test)

		#test = CheckBox("Display Treasures", self.gui, offset=(25, 650))
		#test.name = "displaytreasure"
		#self.gui.add_component(test)

		test = OrangeLabel("Time Running", "0.0", self.gui, offset=(25, 730))
		test.name = "time"
		self.gui.add_component(test)

		test = OrangeLabel("FPS", "0.0", self.gui, offset=(25, 750))
		test.name = "fps"
		self.gui.add_component(test)

		self.thread = None

	#def dopath(self):
	#	sleep(5)

	def update(self, time, events):
		'''
		if self.thread is None or not self.thread.isAlive():
			print("calculating path")
			self.thread = Thread(target=self.dopath)
			self.thread.start()
		'''
		'''
		if time > 0.017:
			self.catchup = abs(time - (0.017))
			print time
		'''
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
		self.mapimg = pygame.image.load(json_settings["map_img"])
		self.rect = self.mapimg.get_rect()
		self.blit(self.mapimg, self.rect)
		self.landmarks = []
		self.display_treasures = False
		for landmark in json_settings["landmarks"]:
			self.landmarks.append(Landmark(**landmark))

		self.update_timer = 0

		self.known_entities = []
		place = 100
		col = 0
		row = 0
		for i in range(0, 2):
			col += 1
			robot = Robot(self)
			print i*place
			robot.rect.x, robot.rect.y = col*place, place*row
			robot.x, robot.y = col*place, place*row
			self.known_entities.append(robot)
			if col > 4: col = 0; row += 1
		self.robot = self.known_entities[0]

		self.known_entities[0].type = ""

		self.treasures = []

		self.treasures.append(Treasure(self))
		self.treasures.append(Treasure(self))
		self.treasures.append(Treasure(self))

	def update(self, time, events):

		for entity in self.known_entities:
			self.blit(self.mapimg.subsurface(entity.previous_rect.x, entity.previous_rect.y, entity.previous_rect.width, entity.previous_rect.height), entity.previous_rect)
		
		# do some updates to the gui
		if self.update_timer > 0.25:
			self.update_timer = 0
			EventDispatcher().send_event(LabelChange("bearing", str(self.robot.bearing)))
			EventDispatcher().send_event(LabelChange("position", "(" + str(self.robot.rect.x) + ", " + str(self.robot.rect.y) + ")"))

			points = pygame.sprite.spritecollide(self.robot, self.landmarks, False)
			if len(points) > 0:
				loc = ""
				for landmark in points:
					loc += landmark.name + "/"
				EventDispatcher().send_event(LabelChange("location", loc))

			else:
				EventDispatcher().send_event(LabelChange("location", "N/A"))


			EventDispatcher().send_event(LabelChange("bearingai", str(self.known_entities[1].bearing)))
			EventDispatcher().send_event(LabelChange("positionai", "(" + str(self.known_entities[1].rect.x) + ", " + str(self.known_entities[1].rect.y) + ")"))

			points = pygame.sprite.spritecollide(self.known_entities[1], self.landmarks, False)
			if len(points) > 0:
				loc = ""
				for landmark in points:
					loc += landmark.name + "/"
				EventDispatcher().send_event(LabelChange("locationai", loc))

			else:
				EventDispatcher().send_event(LabelChange("locationai", "N/A"))

		self.update_timer += time

		'''
		if len(self.treasures) is not 3:
			self.treasures.append(Treasure(self))
			self.treasures.append(Treasure(self))
			self.treasures.append(Treasure(self))
		'''

		for treasure in self.treasures:
			collision = False
			for entity in self.known_entities:
				if entity.rect.colliderect(treasure.rect):
					collision = True
					self.blit(self.mapimg.subsurface(treasure.rect.x, treasure.rect.y, treasure.rect.width, treasure.rect.height), treasure.rect)
					entity.score += treasure.score
					EventDispatcher().send_event(LabelChange(str("score"+entity.type), str(entity.score)))
					self.treasures.remove(treasure)
					continue
			if not collision:
				self.blit(self.mapimg.subsurface(treasure.rect.x, treasure.rect.y, treasure.rect.width, treasure.rect.height), treasure.rect)
				treasure.update(time, events)

		for entity in self.known_entities:
			entity.update(time, events)

		if len(self.treasures) == 0:
			for i in range(0, 3):
				self.treasures.append(Treasure(self))

		self.parent.blit(self, self.rect)

	# override the blit method in case we need to do anything with it later on
	def blit(self, surface, rect):
		super(Level, self).blit(surface, rect)

	def event_handler(self, event):
		if event.istype(CheckBoxEvent) and event.name is "displaypath":
			if event.checked:
				self.color = (255, 255, 255)
			else:
				self.color = (0, 0, 0)
		if event.istype(ButtonClickEvent) and event.name == "position":
			EventDispatcher().send_event(LabelChange("position", str(self.x)))
		if event.istype(ButtonClickEvent) and event.name is "menu":
			EventDispatcher().send_event(LevelChangeEvent(None, LEVEL_MAIN_MENU))
		if event.istype(SliderEvent) and event.name is "bearing":
			self.robot.bearing = event.slidervalue
			self.robot.timer = 0
		if event.istype(SliderEvent) and event.name is "velocity":
			self.robot.velocity = event.slidervalue
		if event.istype(SliderEvent) and event.name is "velocityai":
			self.known_entities[1].velocity = event.slidervalue
		if event.istype(CheckBoxEvent) and event.name is "displaytreasure":
			self.display_treasures = event.checked

class PauseMenu(Level, IEventHandler):

	def __init__(self, parent):
		Level.__init__(self, size=(parent.get_rect().width, parent.get_rect().height))
		IEventHandler.__init__(self)

		self.gui = Gui(self, size=(parent.get_rect().width, parent.get_rect().height), offset=(0, 0))

		test1 = PlayTitle("Paused", self.gui, offset=(parent.get_rect().width / 2 - 35, 300))
		self.gui.add_component(test1)

		test1 = Button("Resume", 2, self.gui, offset=(parent.get_rect().width / 2 - 50, 350))
		test1.name = "resume"
		self.gui.add_component(test1)

		#test1 = FlashingLabel("Testing", self.gui, offset=(self.gui.rect.center[0]-50, 200))
		#test1.name = "test"
		#self.gui.add_component(test1)
		self.init = False

	def update(self, time, events):
		self.gui.update(time, events)

	def event_handler(self, event):
		'''
		if event.istype(ButtonClickEvent) and event.name is "start":
			EventDispatcher().send_event(LevelChangeEvent("test", LEVEL_GAME))
		'''
		pass