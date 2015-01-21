import pygame
from engine.Engine import GameEngine
from map.Levels import MainMenu, GameLevel


gameengine = GameEngine()
gameengine.change_level(MainMenu())
gameengine.mainloop()

pygame.quit()