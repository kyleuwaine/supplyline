import pygame
from enum import Enum
import SLFaction

class SLBrigade:
    class BrigadeType(Enum):
        TANK = 0

    def __init__(self, brigade_type: str, faction):
        match brigade_type:
            case "Tank":
                self.type = SLBrigade.BrigadeType.TANK
                self.sprite = "Images\ight_arrow.png"
            case _:
                assert 0 == 1, "Invalid Brigade Type"
        self.health = 100
        self.faction = faction
        self.pygame_surface = pygame.image.load(self.sprite)
