import pygame
from gui.Components import *

class Gui(pygame.Surface):

	# the main background color
	BACKGROUND = (242, 242, 242)

	def __init__(self, parent, size=(100, 100), offset=(0, 0), background=(242, 242, 242), **kwargs):
		pygame.Surface.__init__(self, size, **kwargs)
		self.components = []
		self.parent = parent
		self.rect = self.get_rect()
		self.rect.x, self.rect.y = offset[0], offset[1]
		self.background = background
		self.fill(self.background)

	def add_component(self, component):
		self.components.append(component)

	def update(self, timer, events):
		#print timer
		#surf = pygame.Surface((100, 100))
		#surf.fill((0, 0, 0))
		update = False
		#self.fill(self.background)
		for component in self.components:
			if update is True:
				component.update(timer, events)
			else:
				update = component.update(timer, events)
		#self.blit(surf, surf.get_rect())
		if update:
			self.parent.blit(self, self.rect)