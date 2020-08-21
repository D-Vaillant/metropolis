import random

from components.ai import HostileEnemy
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item

player = Actor(
    char="@",
    color=(255,255,255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(body=15,
                    agility=5,
                    reflexes=5,
                    strength=7,
                    charisma=5,
                    intuition=5,
                    logic=5,
                    willpower = 5),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(body=10,
                    agility=5,
                    reflexes=5,
                    strength=3,
                    charisma=5,
                    intuition=5,
                    logic=5,
                    willpower = 5),
    inventory=Inventory(capacity=0),
)

troll = Actor(
    char="T",
    color=(0,127,0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(body=15,
                    agility=5,
                    reflexes=5,
                    strength=10,
                    charisma=5,
                    intuition=5,
                    logic=5,
                    willpower = 5),
    inventory=Inventory(capacity=0),
)

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=(lambda: (random.randint(1, 4)+2))),
)

lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
