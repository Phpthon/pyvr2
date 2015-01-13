import pygame
from event.EventHandler import IEventHandler, EventDispatcher
from event.Events import ButtonClickEvent, SliderEvent, CheckBoxEvent, LabelChange
from misc.Constants import *
import math

class Component(pygame.Surface, IEventHandler):

	def __init__(self, size, parent, offset=(0, 0), name="untitled", **kwargs):

		pygame.Surface.__init__(self, size, **kwargs)
		self.rect = self.get_rect().copy()
		self.rect.x += offset[0]
		self.rect.y += offset[1]

		self.parent = parent
		self.event_rect = self.rect.copy()
		self.event_rect.x, self.event_rect.y = parent.rect.x + offset[0], parent.rect.y + offset[1]
		self.name = name

	def update(self, timer):
		pass

class Button(Component):

	def __init__(self, size, parent, **kwargs):

		Component.__init__(self, size, parent, **kwargs)
		#self.fill((220,20,60))
		self.clicked = False
		self.hovered = False
		self.init = False

		self.counter = 0


	def update(self, timer, events):
		update = False
		for event in events:
			if event.type == pygame.MOUSEMOTION:
				if self.event_rect.collidepoint(event.pos):
					update = True
					self.hovered = True
				else:
					if self.clicked or self.hovered:
						update = True
					self.clicked = False
					self.hovered = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.event_rect.collidepoint(event.pos):
					if not self.clicked:
						self.counter += 1
						EventDispatcher().send_event(ButtonClickEvent(self.name, str(self.counter)))
					self.clicked = True
					update = True
			if event.type == pygame.MOUSEBUTTONUP:
				if self.event_rect.collidepoint(event.pos):
					update = True
					self.clicked = False

		if update or not self.init:
			self.init = True
			if self.hovered:
				if self.clicked:
					self.fill((128,128,0))
				else:
					self.fill((255,0,0))
			else:
				self.fill((255,255,0))
			self.parent.blit(self, self.rect)
			return True
		return False

class CheckBox(Component):

	sprites = pygame.image.load("assets/img/checkbox_sprites.png")

	def __init__(self, name, parent, **kwargs):
		Component.__init__(self, (210, 16), parent, **kwargs)

		self.clicked = False
		self.hovered = False
		self.init = False
		self.checked = False

		self.counter = 0

		self.font = pygame.font.Font(FONT_REGULAR, 12).render(name, True, (92, 92, 92))
		self.bg = CheckBox.sprites.subsurface((0, 0, 16, 16))
		self.bg_hover = CheckBox.sprites.subsurface((0, 16, 16, 16))
		self.tick = CheckBox.sprites.subsurface((0, 32, 16, 14))

	def update(self, timer, events):
		update = False
		for event in events:
			if event.type == pygame.MOUSEMOTION:
				if self.event_rect.collidepoint(event.pos):
					update = True
					self.hovered = True
				else:
					if self.hovered:
						update = True
					self.hovered = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.event_rect.collidepoint(event.pos):
					if self.checked:
						self.checked = False
						EventDispatcher().send_event(CheckBoxEvent(self.name, self.checked))
					else:
						self.checked = True
						EventDispatcher().send_event(CheckBoxEvent(self.name, self.checked))
					update = True

		if update or not self.init:
			self.init = True
			self.fill(self.parent.background)
			
			if self.hovered:
				self.blit(self.bg_hover, (0, 0))
			else:
				self.blit(self.bg, (0, 0))
			if self.checked:
				self.blit(self.tick, (2,0))
			self.blit(self.font, (26, 3))

			self.parent.blit(self, self.rect)
			return True
		return False

class Title(Component):

	sprites = pygame.image.load("assets/img/title_sprites.png")

	def __init__(self, title, parent, sprite, **kwargs):
		Component.__init__(self, (210, 38), parent, **kwargs)
		self.sprite = Title.sprites.subsurface((0, sprite * 16, 16, 16))
		self.font = pygame.font.Font(FONT_REGULAR, 12).render(title, True, (0, 0, 0))
		self.init = False

	def update(self, timer, events):
		if not self.init:
			self.init = True
			self.fill(self.parent.background)
			self.blit(self.sprite, (10, 10))
			self.blit(self.font, (40, 13))
			pygame.draw.line(self, (212, 212, 212), (0, self.rect.height-1), (self.rect.width, self.rect.height-1))
			self.parent.blit(self, self.rect)

			return True
		return False

class OrangeLabel(Component, IEventHandler):

	sprites = pygame.image.load("assets/img/title_sprites.png")

	def __init__(self, title, value, parent, **kwargs):
		Component.__init__(self, (210, 16), parent, **kwargs)
		IEventHandler.__init__(self)
		self.font = pygame.font.Font(FONT_REGULAR, 12)
		self.title = self.font.render(title, True, (92, 92, 92))
		self.value = self.font.render(value, True, (228, 174, 46))
		self.init = False
		self.test = 0

	def update(self, timer, events):

		if not self.init:

			self.init = True
			self.fill(self.parent.background)
			#self.blit(self.sprite, (10, 10))
			self.blit(self.title, (0, 0))
			self.blit(self.value, (self.get_rect().width - self.value.get_rect().width, 0))
			
			self.parent.blit(self, self.rect)

			return True
		return False

	def event_handler(self, event):
		if event.istype(LabelChange) and event.name is self.name:
			self.value = self.font.render(event.string, True, (228, 174, 46))
			self.init = False

class Slider(Component):

	slider_sprites = None

	def __init__(self, parent, offset=(0, 0), **kwargs):
		Component.__init__(self, (210, 38), parent, offset, **kwargs)

		if Slider.slider_sprites == None:
			sprites = pygame.image.load("assets/img/slider_sprites.png")
			Slider.slider_sprites = [
				sprites.subsurface((0,0,210,13)),
				sprites.subsurface((0,13,210,13)),
				sprites.subsurface((0,26,30,7)),
				sprites.subsurface((0,33,30,7))
			]

		# user options
		self.paddingright = 3
		self.paddingleft = 3
		self.increment = 10
		self.minvalue = 10.0
		self.maxvalue = 100.0
		self.x, self.y = 0, 0

		# init the track
		self.track_rect = Slider.slider_sprites[0].get_rect().copy()
		self.track_rect.x = 0
		self.track_rect.y = 25

		# calc max start/end position of bar
		self.maxright = self.track_rect.right - self.paddingright
		self.maxleft = self.track_rect.x + self.paddingleft

		# init the bar
		self.bar_rect = Slider.slider_sprites[2].get_rect().copy()
		self.bar_rect.x = self.maxleft
		self.bar_rect.y = self.track_rect.y + 3

		self.click = False
		self.offset = None
		self.currentvalue = 0

		# calculate empty space between bar and padded edges along with the ratio
		self.emptyspace = self.maxright - self.maxleft - self.bar_rect.width
		self.ratio = ((self.maxvalue - self.minvalue) / self.increment) / self.emptyspace

		self.track_image = Slider.slider_sprites[0]
		self.bar_image = Slider.slider_sprites[2]

		self.track_rect_event = self.track_rect.copy()
		self.track_rect_event.x = self.track_rect.x + self.event_rect.x
		self.track_rect_event.y = self.track_rect.y + self.event_rect.y

		self.bar_rect_event = self.bar_rect.copy()
		self.bar_rect_event.x = self.bar_rect.x + self.event_rect.x
		self.bar_rect_event.y = self.bar_rect.y + self.event_rect.y

		self.font = pygame.font.Font(FONT_REGULAR, 12)
		self.label = self.font.render("Velocity", True, (92, 92, 92))
		self.init = False

		self.hovered = False
		self.previousvalue = 0

	def update(self, timer, events):

		required = False

		for event in events:
			if event.type == pygame.MOUSEMOTION:
			
				if self.track_rect_event.collidepoint(event.pos):
					self._hovered(True)
					required = True
				elif not self.click and self.hovered:
					self._hovered(False)
					required = True
			if event.type == pygame.MOUSEBUTTONDOWN:

				if self.bar_rect_event.collidepoint(event.pos):
					required = True
					self._hovered_bar(True)
					self.click = True
					if self.offset is None:
						self.offset = event.pos[0] - self.bar_rect.x

			elif event.type == pygame.MOUSEBUTTONUP and self.hovered:
				required = True
				self.click = False
				self.offset = None
				self._hovered_bar(False)

		if required or self.click or not self.init:
			self.init = True
			self.fill(self.parent.background)

			if self.click:
				newpos = pygame.mouse.get_pos()[0] - self.offset
				if newpos + self.bar_rect.width < self.maxright and newpos > self.maxleft:
					self.bar_rect.right = newpos + self.bar_rect.width
					self.bar_rect_event.x = self.track_rect_event.left + self.paddingleft + newpos
				elif newpos + self.bar_rect.width > self.maxright:
					self.bar_rect.right = self.maxright
					self.bar_rect_event.right = self.track_rect_event.right - self.paddingright
				elif newpos < self.maxleft:
					self.bar_rect.left = self.maxleft
					self.bar_rect_event.left = self.track_rect_event.x + self.paddingleft

			self.currentvalue = self.myround( ( (self.bar_rect.right - self.maxright + self.emptyspace ) * self.ratio) * self.increment + self.minvalue, self.increment)
			
			text = self.font.render(str(self.currentvalue), True, (41, 140, 218))


			self.blit(text, (self.track_rect.right - self.paddingright - text.get_rect().width, self.track_rect.y - 20))
			self.blit(self.label, (self.track_rect.left + self.paddingleft, self.track_rect.y - 20))

			self.blit(self.track_image, self.track_rect)
			self.blit(self.bar_image, self.bar_rect)

			#print self.track_rect
			self.parent.blit(self, self.rect)

			if self.currentvalue is not self.previousvalue:
				EventDispatcher().send_event(SliderEvent(self.name, self.currentvalue))
				self.previousvalue = self.currentvalue

			return True
		return False

	def _hovered(self, is_hovered):
		self.hovered = is_hovered
		if is_hovered:
			self.track_image = Slider.slider_sprites[1]
		else:
			self.track_image = Slider.slider_sprites[0]

	def _hovered_bar(self, is_hovered):
		if is_hovered:
			self.bar_image = Slider.slider_sprites[3]
		else:
			self.bar_image = Slider.slider_sprites[2]

	def myround(self, x, base=5):
		return int(base * math.ceil(float(x)/base))

	def event_handler(self, event):
		print "helllo"