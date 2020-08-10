from enum import auto, Enum


class DamageType:
    name: str
    message: str
    weakness: str
    resistance: str


class Force(DamageType):
    name: str = "Force"
    message = "A bolt of force strikes {target_name} for {damage} HP."
    weakness = "{target_name} staggers as the force bolt collides, taking {damage} HP."
    resistance = "{target_name} shrugs off the force bolt, taking {damage} HP."


class Lightning(DamageType):
    name: str = "Lightning"
    message = "A crackle of electricity strikes {target_name} for {damage} HP."
    weakness = message
    resistance = message


class Fire(DamageType):
    name: str = "Fire"


class Blunt(DamageType):
    name: str = "Blunt"


class Piercing(DamageType):
    name: str = "Piercing"


class Slashing(DamageType):
    name: str = "Slashing"
