from enum import Enum
import SLFaction

class SLBrigade:
    class BrigadeType(Enum):
        TANK = 0

    def __init__(brigade_type: str, faction):
        match brigade_type:
            case "Tank":
                self.type = SlBrigade.BrigadeType.TANK
            case _:
                assert 0 == 1, "Invalid Brigade Type"
        self.health = 100
        self.faction = faction